import datetime
from django.db.models import DecimalField, F, ExpressionWrapper, base, fields
from django.db.models.expressions import Case, Exists, When
from django.db.models.query_utils import Q
from apps.planilla.models import *
from apps.planilla.forms import *
from django.shortcuts import get_object_or_404, render
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.db.models import Subquery
import json


#Detalle Planilla
def PlanillaList(request):
    return render(request,'detalle_planilla/detalle_planilla_list.html')


def DetallePlanilla(request):

    try:
        Bases_ley.objects.get(~Q(bonificacion_incentivo__lte=0), estado=True)
    except Bases_ley.DoesNotExist:
        print('COMUNIQUESE CON EL ADMINISTRADOR, NO HAY BASES DE LEY')
        raise Http404
    try:
        Impuesto.objects.get(estado=True, descripcion__icontains = 'igss')
    except Impuesto.DoesNotExist:
        print('COMUNIQUESE CON EL ADMINISTRADOR, NO HAY IGSS REGISTRADO')
        raise Http404
    try:
        Impuesto.objects.get(estado=True, descripcion__icontains = 'isr')
    except Impuesto.DoesNotExist:
        print('COMUNIQUESE CON EL ADMINISTRADOR, NO HAY ISR REGISTRADO')
        raise Http404
    try:
        Impuesto.objects.get(estado=True, descripcion__icontains = 'igss')
    except Impuesto.DoesNotExist:
        print('COMUNIQUESE CON EL ADMINISTRADOR, NO HAY IGSS REGISTRADO')
        raise Http404


    bonIncentivo = Bases_ley.objects.filter(estado=True)[:1]
    igss = Impuesto.objects.filter(estado=True,descripcion__icontains='igss')
    isr = Impuesto.objects.filter(estado=True, descripcion__icontains='isr')
    deudas = Pago_movimiento.objects.filter()

    listadoUser1 = User.objects.filter(ingreso__planilla=True,detalle_puesto__estado=True)\
        .prefetch_related('Puesto')\
        .annotate(horasExtra=ExpressionWrapper(F('ingreso__cantidad_horas_aut')*
                        F('ingreso__valor_horas_extra'),output_field=DecimalField()),
                    bonificacion__in=Subquery(bonIncentivo.values('bonificacion_incentivo')),
                    salarioTotal = ExpressionWrapper(F('detalle_puesto__monto_salario')+F('ingreso__incentivo')+F('bonificacion__in')+
                        F('horasExtra'), output_field=DecimalField()),
                    igssPorcentaje__in = Subquery(igss.values('porcentaje')),
                        multiplicacionIgss = ExpressionWrapper(F('detalle_puesto__monto_salario') * 
                            F('igssPorcentaje__in'),output_field=DecimalField(decimal_places=2)),
                    isrPorcentaje__in = Subquery(isr.values('porcentaje')),
                    isrMonto__in = Subquery(isr.values('monto_minimo')),
                         calculoIsr = ExpressionWrapper((F('detalle_puesto__monto_salario')+F('bonificacion__in')-(F('isrMonto__in')/12)
                            -F('multiplicacionIgss'))*F('isrPorcentaje__in'),output_field=DecimalField(decimal_places=2)),
                            isrTotal = Case(
                                When(calculoIsr__lte = 0, then=0),
                                When(calculoIsr__gt = 0, then=F('calculoIsr'))
                            ),
                    totalDeducciones = ExpressionWrapper(F('multiplicacionIgss')+F('isrTotal'), output_field=DecimalField()),
                    salarioLiquido = ExpressionWrapper(F('salarioTotal')-F('totalDeducciones'), output_field=DecimalField()),
                    )\
        .values('id','first_name','last_name', 'horasExtra','ingreso__valor_horas_extra', 
                'detalle_puesto__monto_salario','puesto__nombre','ingreso__incentivo','bonificacion__in',
                'salarioTotal','multiplicacionIgss', 'isrTotal', 'totalDeducciones', 'salarioLiquido')
    return JsonResponse({'data':list(listadoUser1)})


def detallePlanilla():

    today = datetime.date.today()
    bonIncentivo = Bases_ley.objects.filter(estado=True)[:1]
    igss = Impuesto.objects.filter(estado=True,descripcion__icontains='igss')
    isr = Impuesto.objects.filter(estado=True, descripcion__icontains='isr')

    data = User.objects.filter(ingreso__planilla=True,detalle_puesto__estado=True)\
        .prefetch_related('Puesto')\
        .annotate(horasExtra=ExpressionWrapper(F('ingreso__cantidad_horas_aut')*
                        F('ingreso__valor_horas_extra'),output_field=DecimalField()),
                    bonificacion__in=Subquery(bonIncentivo.values('bonificacion_incentivo')),
                    basesLeyId__in = Subquery(bonIncentivo.values('id')),
                    salarioTotal = ExpressionWrapper(F('detalle_puesto__monto_salario')+F('ingreso__incentivo')+F('bonificacion__in')+
                        F('horasExtra'), output_field=DecimalField()),
                    igssPorcentaje__in = Subquery(igss.values('porcentaje')),
                        multiplicacionIgss = ExpressionWrapper(F('detalle_puesto__monto_salario') * 
                            F('igssPorcentaje__in'),output_field=DecimalField(decimal_places=2)),
                    isrPorcentaje__in = Subquery(isr.values('porcentaje')),
                    isrMonto__in = Subquery(isr.values('monto_minimo')),
                         calculoIsr = ExpressionWrapper((F('detalle_puesto__monto_salario')+F('bonificacion__in')-(F('isrMonto__in')/12)
                            -F('multiplicacionIgss'))*F('isrPorcentaje__in'),output_field=DecimalField(decimal_places=2)),
                            isrTotal = Case(
                                When(calculoIsr__lte = 0, then=0),
                                When(calculoIsr__gt = 0, then=F('calculoIsr'))
                            ),
                    totalDeducciones = ExpressionWrapper(F('multiplicacionIgss')+F('isrTotal'), output_field=DecimalField()),
                    salarioLiquido = ExpressionWrapper(F('salarioTotal')-F('totalDeducciones'), output_field=DecimalField()),
                     )\
        .values('id','first_name','last_name', 'puesto__nombre', 'detalle_puesto__monto_salario', 'ingreso__incentivo', 
                'ingreso__valor_horas_extra', 'horasExtra', 'bonificacion__in', 'salarioTotal','multiplicacionIgss',
                'isrTotal', 'totalDeducciones', 'salarioLiquido', 'basesLeyId__in')
    

    for i in range(len(data)):
        basesLeyId = Bases_ley.objects.get(pk=data[i]['basesLeyId__in'])
        userId = User.objects.get(pk=data[i]['id'])
        detalle = Detalle_planilla(salario_ordinario = data[i]['detalle_puesto__monto_salario'], incentivo = data[i]['bonificacion__in'],\
            bonificaciones = data[i]['ingreso__incentivo'], horas = data[i]['horasExtra'], valor_horas = data[i]['ingreso__valor_horas_extra'],\
            salarioTotal = data[i]['salarioTotal'], cuotaIgss = data[i]['multiplicacionIgss'], descuentoIsr = data[i]['isrTotal'],\
            totalDeducciones = data[i]['totalDeducciones'], liquido = data[i]['salarioLiquido'], fechaCreacion = today, bases_ley_pk = basesLeyId, user = userId)
        detalle.save()
    
    return print('Planilla guardada con éxito')

    
detallePlanilla()


#Movimientos

class MovimientoCreate(CreateView):
    model = Movimiento
    form_class = MovimientoForm
    template_name = 'movimiento/movimiento_form.html'
    success_url = reverse_lazy('planilla:PlanillaList')