import uuid

from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from endereco.api.serializers import AddressSerializer
from endereco.models import Address
from innovation_dreams.utils import store_image
from usuario.models import User, GROUP
from django.contrib.auth.models import User as UserAuth, Group
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from pycpfcnpj import cpfcnpj


class LoginSerializer(ModelSerializer):
    token = SerializerMethodField()
    email = SerializerMethodField()
    user_id = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'token',
            'user_id',
            'email'
        )

    def get_token(self, obj):
        return Token.objects.get(user=obj.auth_user).pk

    def get_email(self, obj):
        return obj.auth_user.email

    def get_user_id(self, obj):
        return obj.id


class UsuarioSerializer(ModelSerializer):

    email = SerializerMethodField()
    address = AddressSerializer()

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
            'blocked',
            'facebook',
            'instagram',
            'linkedin',
            'celular',
            'address',
        )

    def get_email(self, obj):
        return obj.auth_user.email

    def update_address(self, address, data):
        address.street = data['street']
        address.zipCode = data['zipCode']
        address.number = data['number']
        address.state = data['state']
        address.country = data['country']
        address.neighbourhood = data['neighbourhood']
        address.city = data['city']
        address.complement = data['complement']

    def update(self, instance, validated_data):
        self.update_address(instance.address, validated_data['address'])

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

        instance.state = validated_data['blocked']
        instance.facebook = validated_data['facebook']
        instance.instagram = validated_data['instagram']
        instance.linkedin =  validated_data['linkedin']
        instance.celular = validated_data['celular']

        instance.save()

        return instance


class CreateUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=15)
    fullName = serializers.CharField(max_length=300)
    profile = serializers.CharField(max_length=1)

    def create(self):
        userAuth = UserAuth.objects.filter(email=self.data['email'])
        if len(userAuth) != 0:
            raise Exception("Usuário já cadastrado, fala xande")

        userAuth = UserAuth.objects.create_user(username=self.data['email'],
                                                first_name=self.data['fullName'],
                                                password=self.data['password'],
                                                email=self.data['email'])
        fullName = self.data['fullName']
        group = Group.objects.get(name=GROUP[int(self.data['profile'])-1])
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