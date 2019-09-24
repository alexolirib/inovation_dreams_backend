from rest_framework.views import APIView
from rest_framework.response import Response
from usuario.serializers import CreateUserSerializer
from django.contrib.auth.models import User as UserAuth
from datetime import datetime
from usuario.models import User

class CriarUsuarioView(APIView):

    def get(self, request, *args, **kwargs):
        result = UserAuth.objects.filter(email="1@gmail.com")
        json = result[0]
        return Response(json)

    def post(self, request, *args, **kwargs):
        try:
            data_serializar = CreateUserSerializer(data=request.data)
            data_serializar.is_valid(raise_exception=True)

            response = User.criar_usuario(data_serializar.data)
            return Response(response, status=201)
        except Exception as e:
            error = {'Error': e.args[0], 'hora': datetime.now()}
            return Response(error, status=400)
