from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet, ViewSet

from usuario.api.serializers import UsuarioSerializer
from usuario.models import User


class UsuarioViewSet(ModelViewSet):
    # http_method_names = ['GET']
    queryset = User.objects.all()
    serializer_class = UsuarioSerializer

    # @action(methods=['post'], detail=False)
    # def criar

class CriarUsuario(ViewSet):
    def create(self, request):
        pass


