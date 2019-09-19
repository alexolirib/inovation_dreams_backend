from django.db import models

class Address(models.Model):
    zipCode = models.CharField(max_length=8)
    street = models.CharField(max_length=180)
    number = models.IntegerField(null=True)
    state = models.CharField(max_length=180)
    neighbourhood = models.CharField(max_length=100)
    city = models.CharField(max_length=180)
    complement = models.CharField(max_length=180, null=True)
