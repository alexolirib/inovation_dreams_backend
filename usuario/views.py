from rest_framework.views import APIView
from rest_framework.response import Response
from usuario.models import User
from datetime import datetime

class CriarUsuarioView(APIView):

    def get(self, request, *args, **kwargs):
        json = {'teste': 'deu certo'}
        return Response(json)

    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            print(data)
            response = User.criar_usuario(data)
            json = response
            return Response(json, status=201)
        except Exception as e:
            error = {'Error': e.args[0], 'hora': datetime.now()}
            return Response(error, status=400)
