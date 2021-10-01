# from django.urls import path
# from django.contrib.auth.decorators import login_required
# from django.urls.resolvers import URLPattern
# from apps.departamento.views import *

# app_name = 'departamento'

# urlpatterns = [
#     path('nuevo', login_required(DepartamentoCreate.as_view()), name='departamento_create'),
#     path('DepartamentoList', login_required(DepartamentoList), name='DepartamentoList'),
#     path('DepartamentoListado', login_required(DepartamentoListado), name='DepartamentoListado'),
#     path('update/<int:pk>/', login_required(DepartamentoUpdate.as_view()), name='departamento_update'),
# ]