from django.db import models

CONTATO_TIPO_ENUM = (
    (1, 'Facebook'),
    (2, 'Instragram'),
    (3, 'Linkedin'),
    (4, 'Celular'),
    (5, 'Telefone')
)


class Contato(models.Model):

    tipo_contato = models.CharField(choices=CONTATO_TIPO_ENUM, max_length=15)
    valor_contato = models.CharField(max_length=150)
