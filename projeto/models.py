from django.db import models
from usuario.models import User


class Category(models.Model):
    name = models.CharField(max_length=1000, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Project(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField()
    summary = models.CharField(max_length=1000)
    views = models.IntegerField(default=0)
    date_creation = models.DateField(auto_now_add=True)
    deadline = models.DateField(null=True, blank=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"


class UserProject(models.Model):
    premium = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='projeto', null=True, blank=True)
