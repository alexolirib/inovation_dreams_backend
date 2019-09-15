from django.contrib import admin
from django.urls import path, include


urlAPI = [
    path('usuario/', include('usuario.urls'))
]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(urlAPI))
]