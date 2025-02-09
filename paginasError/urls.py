# paginasError/urls.py

from django.contrib import admin
from django.urls import path, include
from app.views import index, Error, onepage  # Importa las vistas necesarias

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),  # Ruta para la página de inicio
    path('error/', Error, name='error'),  # Ruta para la página de error
    path('onepage/', onepage, name='onepage'),  # Ruta para la página "onepage"
    path('users/', include('users.urls')),  # Incluye las URLs de la aplicación 'users'
]