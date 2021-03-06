from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from projeto.api.serializers import ProjectSerializer, CreateProjectSerializer, CategorySerializer, \
    CreateCategorySerializer
from projeto.models import Project, Category, UserProject
from usuario.models import User


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == "GET":
            permission_classes = [AllowAny]
        elif self.request.method == "POST":
            if self.action == 'view':
                permission_classes = [AllowAny]
            else:
                permission_classes = [IsAuthenticated]
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

    def update(self, request, *args, **kwargs):
        try:
            project = Project.objects.get(id=kwargs['pk'])
        except:
            return Response({'Destails': 'Projeto não encontrado'}, status=status.HTTP_400_BAD_REQUEST)

        user = UserProject.objects.get(project=project).user
        userAuth = request.user

        if user.id != userAuth.user.id:
            return Response({"Details": "Só é permitido alterar o projeto, pelo criador do projeto "}, status=status.HTTP_401_UNAUTHORIZED)

        data_serializer = CreateProjectSerializer(data=request.data)
        data_serializer.is_valid(raise_exception=True)
        project = data_serializer.update(project, request.data)
        return Response(self.get_serializer(project).data, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=True)
    def user(self, request, pk):
        user = User.objects.get(id=pk)
        user_projects = UserProject.objects.filter(user=user)
        projects = []
        for user_project in user_projects:
            projects.append(user_project.project)
        serializers = ProjectSerializer(projects, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)


    @action(methods=['POST'], detail=True)
    def view(self, request, pk):
        try:
            project = Project.objects.get(id=pk)
        except:
            return Response({"Details": "Projeto não encontrado"}, status=status.HTTP_400_BAD_REQUEST)

        project = ProjectSerializer(project).increment_view()
        return Response(self.get_serializer(project).data, status=status.HTTP_200_OK)


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == "GET":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        data_serializer = CreateCategorySerializer(data=request.data)
        data_serializer.is_valid(raise_exception=True)
        if len(Category.objects.filter(name=request.data['category'])) >= 1:
            return Response({'Details': 'Categoria já existente'}, status=status.HTTP_400_BAD_REQUEST)

        data_serializer.create()
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
