from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from endereco.api.viewsets import AddressViewSet
from usuario.api.viewsets import UsuarioViewSet

router = routers.DefaultRouter()
router.register(r'usuario', UsuarioViewSet)
router.register(r'address', AddressViewSet, base_name='Address')

urlAPI = [
    path('usuario/', include('usuario.urls')),
    path('', include(router.urls))
]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(urlAPI))
]