from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from projeto.api.serializers import ProjectSerializer, CreateProjectSerializer
from projeto.models import Project


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == "GET":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


    def create(self, request, *args, **kwargs):
        if len(request.user.groups.filter(name='inventor')) == 0:
            return Response({'Error': 'usuário precisa ser inventor para criar projeto'}, status=status.HTTP_401_UNAUTHORIZED)
        data_serializer = CreateProjectSerializer(data=request.data)
        data_serializer.is_valid(raise_exception=True)
        project = data_serializer.create(request.user.user)
        return Response(self.get_serializer(project).data, status=status.HTTP_201_CREATED)
