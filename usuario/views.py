from rest_framework.views import APIView
from rest_framework.response import Response
from usuario.serializers import CreateUserSerializer
from django.contrib.auth.models import User as UserAuth
from datetime import datetime
from usuario.models import User

class CriarUsuarioView(APIView):

    def get(self, request, *args, **kwargs):
        userAuth = UserAuth.objects.filter(email="13@gmail.com")
        user = User.objects.get_user_fom_user_auth_json(user_auth=userAuth[0])

        return Response(user, status=200)

    def post(self, request, *args, **kwargs):
        # try:
        data_serializar = CreateUserSerializer(data=request.data)
        data_serializar.is_valid(raise_exception=True)

        json = User.criar_usuario(data_serializar.data)

        return Response(json, status=201)
        # except Exception as e:
        #     error = {'Error': e.args[0], 'hora': datetime.now()}
        #     return Response(error, status=400)
