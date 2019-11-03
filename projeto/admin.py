from django.contrib import admin
from projeto.models import Category, Project, UserProject, ProjectImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    verbose_name = "Category"
    verbose_name_plural = "Categories"

    list_display = ('name',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    verbose_name = "Project"
    verbose_name_plural = "Projects"

    list_display = ('title', 'description', 'summary', 'date_creation',)
    ordering = ('date_creation',)


@admin.register(UserProject)
class UserProjectAdmin(admin.ModelAdmin):
    verbose_name = "UserProject"
    verbose_name_plural = "UserProjects"

    list_display = ('id', 'project', 'user', 'premium')


@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    verbose_name = "ProjectImages"
    verbose_name_plural = "ProjectImages"

    list_display = ('id', 'project', 'image')
    ordering = ('project',)
