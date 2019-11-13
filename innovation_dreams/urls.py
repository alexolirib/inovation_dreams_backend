from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from django.conf.urls.static import static
from django.conf import settings
from endereco.api.viewsets import AddressViewSet
from innovation_dreams.login.login import CustomAuthTokenView
from projeto.api.viewset import ProjectViewSet, CategoryViewSet
from usuario.api.viewsets import UsuarioViewSet

router = routers.DefaultRouter()
router.register(r'usuario', UsuarioViewSet)
router.register(r'project', ProjectViewSet)
router.register(r'category', CategoryViewSet)
urlAPI = [
    path('', include(router.urls)),
    path('login/', CustomAuthTokenView.as_view())
]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(urlAPI)),
    # path('chat/', include('chat.urls')),
    path('chat/', include('chat_2.api.urls', namespace='chat')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)