from django.db import models
from django.contrib.auth.models import User, Group
from contato.models import Contato

GROUP = (
    'inventor',
    'investidor'
)

GENERO = (
    (1, 'Masculino'),
    (2, 'Feminino')
)

ESTADO_CIVIL = (
    (1, 'Solteiro'),
    (2, 'Casado'),
    (3, 'Divorciado'),
    (4, 'Viúvo')

)


class Usuario(models.Model):
    nome = models.CharField(max_length=300)
    idade = models.IntegerField()
    foto = models.CharField(max_length=40, null=True)
    availiacao = models.IntegerField(null=True)
    dt_nascimento = models.DateField()
    naturalidade = models.CharField(max_length=90)
    nacionalidade = models.CharField(max_length=90)
    genero = models.CharField(choices=GENERO, max_length=10)
    estado_civil = models.CharField(choices=ESTADO_CIVIL, max_length=10)
    nome_mae = models.CharField(max_length=180)
    nome_pai = models.CharField(max_length=180, null=True)
    cidade_nascimento = models.CharField(max_length=100)
    estado_nascimento = models.CharField(max_length=100)
    cadastro_finalizado = models.BooleanField(default=False)
    auth_user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)





    @staticmethod
    def criar_usuario(data):
        list_response =[]

        user = create_or_get_user_auth(data)

        return 'sucesso'


    def __str__(self):
        return self.nome


class UsuarioContato(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    contato = models.OneToOneField(Contato, unique=True, on_delete=models.CASCADE)



def create_or_get_user_auth(data):
    try:
        return User.objects.get(email=data['email'])
    except:
        if data['perfil'] == None or data['perfil'] == "":
            raise Exception('É preciso informar qual é o perfil do usuário para ser cadastrado.')
        user = User.objects.create_user(username=data['username'],
                                        password=data['password'],
                                        email=data['email'])
        group = Group.objects.get(name=GROUP[int(data['perfil'])])
        user.groups.add(group)
        return user
