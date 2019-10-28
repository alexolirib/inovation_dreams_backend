from tokenize import Token

from django.contrib.auth.decorators import login_required
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, ViewSet

from usuario.api.serializers import UsuarioSerializer, CreateUserSerializer
from usuario.models import User


class UsuarioViewSet(ModelViewSet):
    # http_method_names = ['GET']
    queryset = User.objects.all()
    serializer_class = UsuarioSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #
    #     if self.request.method == "POST":
    #         self.permission_classes = (permission'')

    def get_permissions(self):
        if self.request.method == "POST":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def retrieve(self, request, *args, **kwargs):
        return super(UsuarioViewSet, self).retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return self.criar(request)

    def update(self, request, *args, **kwargs):
        userAuth = request.user
        user = User.objects.get(id=kwargs['pk'])
        if userAuth.user.id != user.id:
            raise Exception("Um usuário está tentando fazer alteração de outro usuário!")

        user = UsuarioSerializer(user).update(user, request.data)

        return Response(self.get_serializer(user).data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=False)
    def criar(self, request):
        data_serializar = CreateUserSerializer(data=request.data)
        data_serializar.is_valid(raise_exception=True)
        user = data_serializar.create()
        serializer = UsuarioSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



