import uuid

from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from endereco.api.serializers import AddressSerializer
from endereco.models import Address
from usuario.models import User, UserContact, GROUP
from django.contrib.auth.models import User as UserAuth, Group
from rest_framework import serializers
from rest_framework.authtoken.models import Token


class UserContactSerializer(ModelSerializer):
    id = SerializerMethodField()
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

    def get_id(self, obj):
        return obj.contact.id



class UsuarioSerializer(ModelSerializer):

    email = SerializerMethodField()
    # contacts = serializers.Field(source='usercontact_set')
    contacts = UserContactSerializer(many=True)
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
        user_contact_list = []
        for data in data_list:
            #verifica se tem id
            if data.get('id'):
                userContact = contacts.filter(contact=data['id'])
                if not userContact:
                    raise Exception("Tentando atualizar um contato de outro usuário")
                userContact = userContact[0]
                userContact.contact.type = data['type']
                userContact.contact.value = data['value']
                user_contact_list.append(userContact)

            # if contacts.filter(contact__type=data['type'], contact__value=data['value']).count() == 0:
            #     contact = Contact(type=data['type'], value=data['value'])
                # UserContact(user=)
                # contacts.add(Contact())
        return user_contact_list




    def update(self, instance, validated_data):
        self.update_address(instance.address, validated_data['address'])
        user_contact_list = self.update_contacts(instance, validated_data['contacts'])

        UserContact.objects.bulk_create_or_update(user_contact_list)
        instance.save()

        return self

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