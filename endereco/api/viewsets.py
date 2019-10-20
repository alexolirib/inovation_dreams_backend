from rest_framework.viewsets import ModelViewSet

from endereco.api.serializers import AddressSerializer
from endereco.models import Address
from usuario.models import User


class AddressViewSet(ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

