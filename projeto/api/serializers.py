from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from projeto.models import Project, Category, ProjectImage


class CategorySerializer(ModelSerializer):

    category = SerializerMethodField()

    class Meta:
        model = Category
        fields = ('category',)

    def get_category(self, obj):
        return obj.name


class ProjectImageSerializer(ModelSerializer):

    class Meta:
        model = ProjectImage
        fields = ('image',)


class ProjectSerializer(ModelSerializer):

    images = ProjectImageSerializer(many=True)
    categories = CategorySerializer(many=True)

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
            'categories',
            'images'
        )

# class ListImageSerialize(serializers.Serializer):
#     image = serializers.ImageField()
#
#
# class ListCategorySerialize(serializers.Serializer):
#     category = serializers.CharField(max_length=1000)


class CreateProjectSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=500)
    description = serializers.CharField(max_length=4000)
    summary = serializers.CharField(max_length=1000)
    deadline = serializers.DateField(allow_null=True)
    budget = serializers.DecimalField(max_digits=10, decimal_places=2, allow_null=True)
    categories = CategorySerializer(many=True)
    images = ProjectImageSerializer(many=True, allow_null=True)

    def validate(self, data):
        error = {}
        if len(data['categories']) == 0:
            error['categories'] = ['O projeto tem que se relacionar com pelomenos uma categoria']
        else:
            for category in data['categories']:
                if category.get('category'):
                   if len(Category.object.filter(name=category['category'])) == 0:
                       error['categories'] = ['Categoria %s está incorreta. Categorias disponíveis são %s' % (category['category'], Category.object.all())]
                       break
                else:
                    error['categories'] = ['Em categories, tem que ter o atributo category']
                    break

        if error != {}:
            raise serializers.ValidationError(error)

        return data
