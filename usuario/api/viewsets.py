from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, ViewSet

from usuario.api.serializers import UsuarioSerializer, CreateUserSerializer
from usuario.models import User


class UsuarioViewSet(ModelViewSet):
    # http_method_names = ['GET']
    queryset = User.objects.all()
    serializer_class = UsuarioSerializer

    @action(methods=['post'], detail=False)
    def criar(self, request):
        data_serializar = CreateUserSerializer(data=request.data)
        data_serializar.is_valid(raise_exception=True)
        user = data_serializar.create()
        serializer = UsuarioSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



