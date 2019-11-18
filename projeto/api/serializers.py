from django.db import transaction
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from datetime import date, datetime

from innovation_dreams.utils import store_image, delete_image
from projeto.models import Project, Category, ProjectImage, UserProject


class CategorySerializer(ModelSerializer):
    category = SerializerMethodField()

    class Meta:
        model = Category
        fields = ('category',)

    def get_category(self, obj):
        return obj.name


class CreateCategorySerializer(serializers.Serializer):
    category = serializers.CharField(max_length=1000)

    def create(self):
        Category.objects.create(name=self.data['category'])


class ProjectImageSerializer(ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = ('image',)


class ProjectSerializer(ModelSerializer):
    images = ProjectImageSerializer(many=True)
    categories = CategorySerializer(many=True)
    user = SerializerMethodField()

    class Meta:
        model = Project
        fields = (
            'id',
            'user',
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

    def get_user(self, obj):
        return obj.userproject_set.last().user.id

    def increment_view(self):
        view  = self.data['views']
        project = Project.objects.get(id=self.data['id'])
        project.views = view +1
        project.save()
        return project


class CreateProjectSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=500)
    description = serializers.CharField(max_length=4000, allow_null=True)
    summary = serializers.CharField(max_length=1000)
    deadline = serializers.DateField(allow_null=True)
    budget = serializers.DecimalField(max_digits=10, decimal_places=2, allow_null=True)
    categories = serializers.ListField()
    images = serializers.ListField()

    def validate(self, data):
        error = {}

        if len(data) <= 3:
            error['title'] = ['O título tem que ter pelomenos 3 caracteres']

        if len(data['categories']) == 0:
            error['categories'] = ['O projeto tem que se relacionar com pelomenos uma categoria']
        else:
            for category in data['categories']:
                if category.get('category'):
                    if len(Category.objects.filter(name=category['category'])) == 0:
                        categories = [x.name for x in Category.objects.all()]
                        error['categories'] = [
                            "Categoria com valor '%s' está incorreta. Categorias disponíveis são %s" % (
                            category['category'], categories)]
                        break
                else:
                    error['categories'] = ['Em categories, tem que ter um objeto com atributo category']
                    break
        if date.today() > data['deadline']:
            error['deadline'] = [
                'O campo prazo não pode ser inferior à data presente - %s' % date.today().strftime("%d/%m/%Y")]

        for image in data['images']:
            if not image.get('image'):
                error['images'] = ['Em images, tem que ter um objeto com atributo image']
                break

            if '/media/project/' in image['image']:
                continue
            try:
                image = image['image'].split(',')
                if ';base64' not in image[0] or 'data:' not in image[0]:
                    raise Exception("Error")
            except:
                error['images'] = ['Imagem não foi enviada de forma correta.']
                break

        if error != {}:
            raise serializers.ValidationError(error)
        return data


    def create_categories(self, project, categories):
        for category_data in categories:
            cat = Category.objects.get(name=category_data['category'])
            project.categories.add(cat)

    @transaction.atomic
    def create(self, user):
        data = self.data
        categories = data['categories']
        del data['categories']
        images = data['images']
        del data['images']

        project = Project.objects.create(**data)
        self.create_categories(project=project, categories=categories)
        project.save()

        if images is not None:
            for image_data in images:
                photo = image_data['image'].split(',')
                image64 = photo[1]
                image = store_image(
                    directory='project',
                    photo_name="%s - %s - %s" % (user.id, project.title, str(datetime.now())),
                    image64=image64
                )

                ProjectImage.objects.create(project=project, image=image)

        UserProject.objects.create(user=user, project=project)

        return project

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.title = validated_data['title']
        instance.description = validated_data['description']
        instance.summary = validated_data['summary']
        instance.deadline = validated_data['deadline']
        instance.budget = validated_data['budget']

        new_categories_values= [x['category'] for x in validated_data['categories']]
        new_categories = []
        for category_value in new_categories_values:
            new_categories.append(Category.objects.get(name=category_value))
        instance.categories.set(new_categories)
        image_to_verify = []
        image_to_stored = []

        validated_data['images'] = [x['image'] for x in validated_data['images']]
        for image_data in validated_data['images']:

            if '/media/project/' in image_data:
                image_to_verify.append(image_data)
            else:
                image_to_stored.append(image_data)
        image_to_remove = []
        for projectImage in instance.images.all():

            image_exist = list(filter(lambda x: projectImage.image.url in x,image_to_verify))
            if not image_exist:
                image_to_remove.append(projectImage)

        for image_data in image_to_stored:
            photo = image_data.split(',')
            image64 = photo[1]
            image = store_image(
                directory='project',
                photo_name="%s - %s - %s" % (instance.userproject_set.last().user.id, instance.title, str(datetime.now())),
                image64=image64
            )

            ProjectImage.objects.create(project=instance, image=image)


        instance.save()

        for remove_image in image_to_remove:
            direct_name = str(remove_image.image)
            remove_image.delete()
            delete_image(direct_name)
        return instance