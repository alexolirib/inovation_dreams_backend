from django.db import models

class Documento(models.Model):
    data_expedicao = models.DateTimeField()
    uf = models.CharField(max_length=2)
    cpf = models.CharField(max_length=11)


class RG(Documento):
    num_rg = models.CharField(max_length=13)
    orgao_emissor = models.CharField(max_length=15)


class CNH(Documento):
    num_cnh = models.IntegerField()
    codigo_seguranca = models.IntegerField()


class RNE(Documento):
    num_rne = models.CharField(max_length=8)
