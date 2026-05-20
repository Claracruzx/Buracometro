from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('paginas.urls')),
    path('', include('usuarios.urls')),
    path('principal', include('principal.urls')),
    path('buracos', include('buracos.urls')),
]
