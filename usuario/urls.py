from django.urls import path
from . import views

urlpatterns = [
    path('criar', views.CriarUsuarioView.as_view(), name="create_user")
]