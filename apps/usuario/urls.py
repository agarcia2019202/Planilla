from django.urls import path
from apps.usuario.views import *

app_name = 'usuario'

urlpatterns = [
    path('registrar/', RegistroUsuario.as_view(), name='registrar')
]