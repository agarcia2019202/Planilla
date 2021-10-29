from django.urls import path
from django.contrib.auth.decorators import login_required
from django.urls.resolvers import URLPattern
from apps.planilla.views import *

app_name = 'planilla'

urlpatterns = [
    path('PlanillaPreList', login_required(PlanillaPreList), name='PlanillaPreList'),
    path('DetallePlanilla', login_required(DetallePlanilla), name='DetallePlanilla'),
    path('SaveDetallePlanilla', login_required(saveDetallePlanilla), name='SaveDetallePlanilla'),
    path('PlanillaList', login_required(PlanillaList), name='PlanillaList'),
    path('PlanillaGet', login_required(PlanillaGet), name='PlanillaGet'),
    path('MovimientoCreate', login_required(MovimientoCreate.as_view()), name='MovimientoCreate')
]