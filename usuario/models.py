from django.db import models
from django.contrib.auth.models import User as UserAuth, Group
from contato.models import Contact
from endereco.models import Address
from usuario.managers import UsuarioManager
import uuid

GROUP = (
    'inventor',
    'investidor'
)

GENERO = (
    (1, 'Masculino'),
    (2, 'Feminino')
)


class User(models.Model):
    id = models.CharField(max_length=250,primary_key=True)
    fullName = models.CharField(max_length=300, null=True, blank=True)
    photo = models.CharField(max_length=100, null=True, blank=True)
    birthDate = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=90, null=True, blank=True)
    genre = models.CharField(choices=GENERO, max_length=10, null=True, blank=True)
    cpf = models.CharField(max_length=11, null=True, blank=True)
    state = models.BooleanField(default=True)
    address = models.OneToOneField(Address, null=True, unique=True, on_delete=models.CASCADE)
    auth_user = models.OneToOneField(UserAuth, unique=True, on_delete=models.CASCADE)

    objects = UsuarioManager()

    @staticmethod
    def criar_usuario(data):
        userAuth = UserAuth.objects.filter(email=data['email'])
        if len(userAuth) != 0:
            raise Exception("Usuário já cadastrado")

        userAuth = UserAuth.objects.create_user(username=data['email'],
                                        password=data['password'],
                                        email=data['email'])
        group = Group.objects.get(name=GROUP[int(data['profile'])])
        userAuth.groups.add(group)
        id_user = str(uuid.uuid4())
        address = Address()
        address.save()
        user = User(id=id_user, auth_user=userAuth, address=address)
        user.save()

        json = User.objects.get_user_fom_user_auth_json(user_auth=userAuth)

        return json

    def save(self, **kwargs):
        if not self.id:
            self.id = uuid.uuid4()
        super().save()

    def __str__(self):
        return f"{self.id} - {self.auth_user.email}"


class UsuarioContato(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    contato = models.OneToOneField(Contact, unique=True, on_delete=models.CASCADE)


def create_or_get_user_auth(data):
    try:
        return User.objects.filter(email=data['email'])
    except:
        if data['perfil'] == None or data['perfil'] == "":
            raise Exception('É preciso informar qual é o perfil do usuário para ser cadastrado.')
        user = User.objects.create_user(username=data['username'],
                                        password=data['password'],
                                        email=data['email'])
        group = Group.objects.get(name=GROUP[int(data['perfil'])])
        user.groups.add(group)
        return user
