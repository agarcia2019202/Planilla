from django.urls import path
from django.contrib.auth.decorators import login_required
from django.urls.resolvers import URLPattern
from apps.planilla.views import *

app_name = 'planilla'

urlpatterns = [
    path('PlanillaList', login_required(PlanillaList), name='PlanillaList'),
    path('DetallePlanilla', login_required(DetallePlanilla), name='DetallePlanilla'),
    path('SaveDetallePlanilla', login_required(detallePlanilla), name='SaveDetallePlanilla'),
    path('MovimientoCreate', login_required(MovimientoCreate.as_view()), name='MovimientoCreate')
]