from django.db import models
from contato.models import Contato

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
    nome = models.CharField(max_length=180)
    idade = models.IntegerField()
    email = models.CharField(max_length=50)
    foto = models.CharField(max_length=40)
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


    def criar_usuario(selfs, data):

    def __str__(self):
        return self.nome

class UsuarioContato(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    contato = models.OneToOneField(Contato, unique=True, on_delete=models.CASCADE)

