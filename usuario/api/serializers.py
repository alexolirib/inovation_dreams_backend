from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from usuario.models import User, UserContact
from django.contrib.auth.models import User as UserAuth
from rest_framework import serializers


class UserContactSerializer(ModelSerializer):
    type = SerializerMethodField()
    value = SerializerMethodField()
    class Meta:
        model = UserContact
        fields = (
            'type',
            'value'
        )

    def get_type(self, obj):
        return obj.contact.type

    def get_value(self, obj):
        return obj.contact.value



class UsuarioSerializer(ModelSerializer):

    email = SerializerMethodField()
    # contacts = serializers.Field(source='usercontact_set')
    contacts = UserContactSerializer(read_only=True, many=True)
    # contacts = serializers.SerializerMethodField(source='usercontact_set')

    class Meta:
        model = User
        depth = 1
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
            'contacts',
            # 'usercontact_set'
            'contacts'
            # 'usuarioContato'
        )

    def get_email(self, obj):
        return obj.auth_user.email


class CreateUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=15)
    profile = serializers.CharField(max_length=1)

    # def create(self, validated_data):
    #     return {**validated_data}
    #
    # def update(self, instance, validated_data):
    #     instance.email = validated_data.get('email', instance.email)
    #     instance.password = validated_data.get('password', instance.password)
    #     instance.profile = validated_data.get('profile', instance.profile)
    #     return instance

    def validate(self, data):
        error = {}
        if int(data['profile']) > 2 or int(data['profile']) < 1:
            error['profile'] = ['O profile necessita ser 1 (inventor) ou 2 (investidor)']

        if len(data['password']) < 3:
            error['password'] = ["A senha tem que ter no mínimo 3 caracteres"]

        if len(UserAuth.objects.filter(email=data['email'])) != 0:
            error['email'] = ["Email já cadastrado"]

        if error != {}:
            raise serializers.ValidationError(error)

        return data