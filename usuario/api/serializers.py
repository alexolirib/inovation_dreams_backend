import uuid

from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from contato.models import ContactTypeChoice, Contact
from endereco.api.serializers import AddressSerializer
from endereco.models import Address
from usuario.models import User, UserContact, GROUP
from django.contrib.auth.models import User as UserAuth, Group
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from pycpfcnpj import cpfcnpj

from usuario.utils import store_image


class UserContactSerializer(ModelSerializer):
    # id = SerializerMethodField()
    type = SerializerMethodField()
    value = SerializerMethodField()

    class Meta:
        model = UserContact
        fields = (
            'id',
            'type',
            'value'
        )

    def get_type(self, obj):
        return obj.contact.type

    def get_value(self, obj):
        return obj.contact.value

    # def get_id(self, obj):
    #     return obj.contact.id



class UsuarioSerializer(ModelSerializer):

    email = SerializerMethodField()
    # contacts = serializers.Field(source='usercontact_set')
    contacts = UserContactSerializer(many=True, read_only=True)
    address = AddressSerializer()
    # contacts = serializers.SerializerMethodField(source='usercontact_set')

    class Meta:
        model = User
        # depth = 1
        fields =(
            'id',
            'email',
            'fullName',
            'photo',
            'birthDate',
            'genre',
            'cpf',
            'nationality',
            'state',
            'address',
            'contacts'
        )

    def update_address(self, address, data):
        address.street = data['street']
        address.zipCode = data['zipCode']
        address.number = data['number']
        address.state = data['state']
        address.neighbourhood = data['neighbourhood']
        address.city = data['city']
        address.complement = data['complement']

    def update_contacts(self, user, data_list):
        contacts = user.contacts
        user_contact_list_atual = UserContact.objects.filter(user=user).values_list('id')
        user_contact_list_atual = [x[0] for x in user_contact_list_atual]

        user_contact_list_atualizado = []
        user_contact_list_remove = []

        for data in data_list:

            #verifica se tem id
            if data.get('id'):
                if data['id'] not in user_contact_list_atual:
                    raise Exception("Tentando atualizar um contato de outro usuário")
                user_contact_list_atual.remove(data['id'])

                userContact = contacts.filter(contact=data['id'])
                userContact = userContact[0]
                try:
                    userContact.contact.type = ContactTypeChoice(data['type']).value
                except:
                    contacts = [x.value for x in ContactTypeChoice.all()]
                    raise Exception("É preciso mandar um type de contato válido. Segue os types válidos %s" % str(contacts))
                userContact.contact.value = data['value']
                user_contact_list_atualizado.append(userContact)
            else:
                contact = Contact()
                try:
                    contact.type = ContactTypeChoice(data['type']).value
                except:
                    contacts = [x.value for x in ContactTypeChoice.all()]
                    raise Exception("É preciso mandar um type de contato válido. Segue os types válidos %s" % str(contacts))
                contact.value = data['value']

                user_contact_list_atualizado.append(UserContact(user=user, contact=contact))

        for user_contact_id in  user_contact_list_atual:
            user_contact_list_remove.append(UserContact.objects.get(id=user_contact_id))

        return {"atualizar": user_contact_list_atualizado, "remover": user_contact_list_remove}

    def update(self, instance, validated_data):
        self.update_address(instance.address, validated_data['address'])
        user_contact_list = self.update_contacts(instance, validated_data['contacts'])

        instance.fullName = validated_data['fullName']
        if validated_data['photo'] is not None:
            photo = validated_data['photo'].split(',')
            image64 = photo[1]
            instance.photo = store_image(
                directory='usuario',
                photo_name=instance.id,
                image64=image64
            )
        instance.birthDate = validated_data['birthDate']
        instance.nationality = validated_data['nationality']
        if validated_data['genre'] is not None:
            if validated_data['genre'] == 'M' or validated_data['genre'] == 'F':
                instance.genre = validated_data['genre']
            else:
                raise Exception('Genre tem que ser M ou F')

        if validated_data['cpf'] is not None:
            if not cpfcnpj.validate(validated_data['cpf']):
                raise Exception('CPF Inválido')

            instance.cpf = validated_data['cpf']

        instance.state = validated_data['state']

        UserContact.objects.bulk_create_or_update_or_delete(user_contact_list)
        instance.save()

        return instance

    def get_email(self, obj):
        return obj.auth_user.email


class CreateUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=15)
    fullName = serializers.CharField(max_length=300)
    profile = serializers.CharField(max_length=1)

    def create(self):
        userAuth = UserAuth.objects.filter(email=self.data['email'])
        if len(userAuth) != 0:
            raise Exception("Usuário já cadastrado")

        userAuth = UserAuth.objects.create_user(username=self.data['email'],
                                                first_name=self.data['fullName'],
                                                password=self.data['password'],
                                                email=self.data['email'])
        fullName = self.data['fullName']
        group = Group.objects.get(name=GROUP[int(self.data['profile'])])
        userAuth.groups.add(group)
        id_user = str(uuid.uuid4())
        address = Address()
        address.save()
        user = User(id=id_user, fullName=fullName, auth_user=userAuth, address=address)
        Token.objects.create(user=userAuth)
        user.save()

        return user


    def validate(self, data):
        error = {}
        if int(data['profile']) > 2 or int(data['profile']) < 1:
            error['profile'] = ['O profile necessita ser 1 (inventor) ou 2 (investidor)']

        if len(data['password']) < 3:
            error['password'] = ["A senha tem que ter no mínimo 3 caracteres"]

        if len(UserAuth.objects.filter(email=data['email'])) != 0:
            error['email'] = ["Email já cadastrado"]

        if len(data['fullName'])  < 5:
            error['fullName'] = ["O nome tem que possuir no mínimo 5 caracteres"]

        if error != {}:
            raise serializers.ValidationError(error)

        return data