from django.db import models
from usuario.models import Usuario

class Endereco(models.Model):
    cep = models.CharField(max_length=8)
    nome_endereco = models.CharField(max_length=180)
    num_endereco = models.IntegerField(null=True)
    estado = models.CharField(max_length=180)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=180)
    complemento = models.CharField(max_length=180, null=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
