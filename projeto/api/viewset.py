from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from projeto.api.serializers import ProjectSerializer, CreateProjectSerializer
from projeto.models import Project


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def create(self, request, *args, **kwargs):
        data_serializer = CreateProjectSerializer(data=request.data)
        data_serializer.is_valid(raise_exception=True)
        data_serializer.create()
        return Response('ok', status=status.HTTP_201_CREATED)
