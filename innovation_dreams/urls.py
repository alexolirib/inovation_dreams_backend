from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from django.conf.urls.static import static
from django.conf import settings
from endereco.api.viewsets import AddressViewSet
from innovation_dreams.login.login import CustomAuthTokenView
from usuario.api.viewsets import UsuarioViewSet

router = routers.DefaultRouter()
router.register(r'usuario', UsuarioViewSet)
router.register(r'address', AddressViewSet, base_name='Address')

urlAPI = [
    # path('usuario/', include('usuario.urls')),
    path('', include(router.urls)),
    # path('login/', obtain_auth_token)
    path('login/', CustomAuthTokenView.as_view())
]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(urlAPI))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)