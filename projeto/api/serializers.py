from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ModelSerializer

from projeto.models import Project, Category


class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = ('name',)


class ProjectSerializer(ModelSerializer):

    category = CategorySerializer(many=True)

    class Meta:
        model = Project
        fields = (
            'id',
            'title',
            'description',
            'summary',
            'views',
            'date_creation',
            'deadline',
            'budget',
            'category'
        )

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
