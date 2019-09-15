from rest_framework.views import APIView
from rest_framework.response import Response

class CriarUsuarioView(APIView):

    def get(self, request, *args, **kwargs):
        json = {'teste': 'deu certo'}
        return Response(json)

    def post(self, request, *args, **kwargs):
        data = request.data

        response ={'Response': 'Criado com sucesso'}
        return Response(response,status=201)
