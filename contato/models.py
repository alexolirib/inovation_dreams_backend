from django.db import models

CONTATO_TIPO_ENUM = (
    (1, 'Facebook'),
    (2, 'Instragram'),
    (3, 'Linkedin'),
    (4, 'Celular')
)


class Contact(models.Model):

    type = models.CharField(choices=CONTATO_TIPO_ENUM, max_length=15)
    value = models.CharField(max_length=150)

    @staticmethod
    def criar_lista_contato(contatos):
        # return [x for Contato(Ctipo_contato=x['tipo'], valor_contato=x['valor']) in contatos]
        return [Contact(tipo_contato=x['tipo'], valor_contato=x['valor']) for x in contatos]
