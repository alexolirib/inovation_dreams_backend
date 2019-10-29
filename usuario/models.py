from enum import Enum

from django.db import models
from django.contrib.auth.models import User as UserAuth
from contato.models import Contact
from endereco.models import Address
import uuid

from usuario.managers import UserContactManage

GROUP = (
    'inventor',
    'investidor'
)


class User(models.Model):
    id = models.CharField(max_length=250, blank=True, primary_key=True)
    fullName = models.CharField(max_length=300, null=True, blank=True)
    photo = models.ImageField(upload_to='usuario', null=True, blank=True)
    birthDate = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=90, null=True, blank=True)
    genre = models.CharField(max_length=1, null=True, blank=True)
    cpf = models.CharField(max_length=11, null=True, blank=True)
    state = models.BooleanField(default=True)
    address = models.OneToOneField(Address, null=True, blank=True, unique=True, on_delete=models.CASCADE)
    auth_user = models.OneToOneField(UserAuth, unique=True, on_delete=models.CASCADE)

    def save(self, **kwargs):
        if not self.id:
            self.id = uuid.uuid4()
        super(**kwargs).save()

    def __str__(self):
        return f"{self.id} - {self.auth_user.email}"


class UserContact(models.Model):
    user = models.ForeignKey(User, related_name='contacts', on_delete=models.CASCADE)
    contact = models.OneToOneField(Contact, null= True, blank=True, unique=True, on_delete=models.CASCADE)

    objects = UserContactManage()
