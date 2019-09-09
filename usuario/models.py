from django.db import models

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
    availiacao = models.IntegerField(null=None)
    telefone1 = models.CharField(max_length=12)
    telefone2 = models.CharField(max_length=12, null=None)
    dt_nascimento = models.DateField()
    naturalidade = models.CharField(max_length=90)
    nacionalidade = models.CharField(max_length=90)
    genero = models.CharField(choices=GENERO)
    estado_civil = models.CharField(choices=ESTADO_CIVIL)
    nome_mae = models.CharField(max_length=180)
    nome_pai = models.CharField(max_length=180, null=None)
    cidade_nascimento = models.CharField(max_length=100)
    estado_nascimento = models.CharField(max_length=100)
