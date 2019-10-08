from enum import Enum

from django.db import models

class ContactTypeChoice(Enum):
    face = 'Facebook'
    insta = 'Instagram'
    linke = 'Linkedin'
    cel = 'Celula'

    @classmethod
    def all(self):
        return [
            ContactTypeChoice.face,
            ContactTypeChoice.insta,
            ContactTypeChoice.linke,
            ContactTypeChoice.cel
        ]

class Contact(models.Model):

    type = models.CharField(
        choices=[(tag.value, tag.name) for tag in ContactTypeChoice.all()]
        , max_length=15
    )
    value = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.type} - {self.value}"

    @staticmethod
    def criar_lista_contato(contatos):
        # return [x for Contato(Ctipo_contato=x['tipo'], valor_contato=x['valor']) in contatos]
        return [Contact(tipo_contato=x['tipo'], valor_contato=x['valor']) for x in contatos]
