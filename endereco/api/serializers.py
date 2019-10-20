from rest_framework.serializers import ModelSerializer
from endereco.models import Address


class AddressSerializer(ModelSerializer):
    class Meta:
        model = Address
        fields = ['zipCode', 'street']
