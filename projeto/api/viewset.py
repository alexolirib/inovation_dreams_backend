from rest_framework.viewsets import ModelViewSet

from projeto.api.serializers import ProjectSerializer
from projeto.models import Project


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
