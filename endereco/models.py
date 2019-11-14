from django.db import models

class Address(models.Model):
    zipCode = models.CharField(max_length=8, null=True, blank=True)
    street = models.CharField(max_length=180, null=True, blank=True)
    number = models.IntegerField(null=True, blank=True)
    state = models.CharField(max_length=180, null=True, blank=True)
    country = models.CharField(max_length=180, null=True, blank=True)
    neighbourhood = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=180, null=True, blank=True)
    complement = models.CharField(max_length=180, null=True, blank=True)

