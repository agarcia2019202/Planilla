import datetime
from django.db.models import Sum
from django.db.models.aggregates import Count
from django.db.models.fields import FloatField, IntegerField
from django.db.models.functions import Concat
from django.db.models import DecimalField, F, ExpressionWrapper, Subquery
from django.db.models.expressions import Case, OuterRef, When
from django.db.models.query_utils import Q
from apps.planilla.models import *
from apps.planilla.forms import *
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect, Http404
from calendar import monthrange
from django.db.models.functions import Coalesce    
from django.db.models import Value as V


#Detalle Planilla
def PlanillaPreList(request):
    #Enviar formulario (input, img, button)    
    return render(request,'detalle_planilla/planilla_prelist.html')


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
        Impuesto.objects.get(estado=True, descripcion__icontains = 'isr', monto_minimo__gte = 48000)
    except Impuesto.DoesNotExist:
        print('COMUNIQUESE CON EL ADMINISTRADOR, NO HAY ISR REGISTRADO CORRECTAMENTE')
        raise Http404

    getMes = request.POST['mes']
    global mes
    mes = int(getMes)    
    today = datetime.date.today()
    dataMes = monthrange(today.year, mes)
    diasMes = dataMes[1]
    
    bonIncentivo = Bases_ley.objects.filter(estado=True)
    igss = Impuesto.objects.filter(estado=True,descripcion__icontains='igss')
    isr = Impuesto.objects.filter(estado=True, descripcion__icontains='isr')

    deudas = Pago_movimiento.objects.filter(fecha__month=mes, fecha__year = today.year, estado=True, movimiento__user = OuterRef('pk')).order_by().values('movimiento__user')

    totalDeudas = deudas.annotate(montoDeudas=Coalesce(Sum(F('monto') ), V(0), output_field=FloatField())).values('montoDeudas')

    listadoUser1 = User.objects.filter(ingreso__planilla=True,detalle_puesto__estado=True)\
        .prefetch_related('puesto', 'movimiento')\
        .annotate(diasCompletos = Count('detalle_reloj__fecha', filter=Q(detalle_reloj__fecha__month = mes, detalle_reloj__fecha__year = today.year, 
                        detalle_reloj__horasTrabajadas__gte = F('detalle_puesto__jornada'))),
                            diasPermiso = Count('detalle_reloj__fecha', filter=Q(detalle_reloj__fecha__month = mes, detalle_reloj__fecha__year = today.year,
                                detalle_reloj__diaConPermiso = True)),
                    totalDias = Coalesce(F('diasCompletos') + F('diasPermiso'), V(0), output_field=DecimalField()),
                    horasDia = Sum('detalle_reloj__horasTrabajadas', filter=Q(detalle_reloj__fecha__month = mes, detalle_reloj__fecha__year = today.year, 
                        detalle_reloj__sePaga = True)),
                    pagoHoras = Coalesce(F('detalle_puesto__monto_salario')/diasMes/F('detalle_puesto__jornada')*F('horasDia'), V(0), output_field=DecimalField()),
                    salarioDevengado = ExpressionWrapper( (F('detalle_puesto__monto_salario')/diasMes * F('totalDias')) + F('pagoHoras'), output_field=DecimalField()),
                    counterHorasE = Sum('detalle_reloj__horasExtra', filter=Q(detalle_reloj__fecha__month = mes, detalle_reloj__fecha__year = today.year)),
                        cantidadHorasE = Case(
                        When(Q(ingreso__cantidad_horas_aut= 0) | Q(counterHorasE = None), then=0),
                        When(counterHorasE__gt = F('ingreso__cantidad_horas_aut'), then=F('ingreso__cantidad_horas_aut')),
                        When(counterHorasE__lte = F('ingreso__cantidad_horas_aut'), then=F('counterHorasE'))
                        ),
                            horasExtra = Case(
                                When(ingreso__aplica_hora_extra = False, then=0),
                                When(ingreso__aplica_hora_extra = True, then=ExpressionWrapper(( F('detalle_puesto__monto_salario')/diasMes) /F('detalle_puesto__jornada')
                                * F('ingreso__valor_horas_extra')*F('cantidadHorasE'),output_field=DecimalField()))
                            ),
                    bonificacion__in=Subquery(bonIncentivo.values('bonificacion_incentivo')),
                        incentivo = ExpressionWrapper( F('bonificacion__in') / diasMes * F('diasCompletos'), output_field=DecimalField()),
                    devengadoTotal = ExpressionWrapper(F('salarioDevengado')+F('ingreso__incentivo')+F('incentivo')+
                        F('horasExtra'), output_field=DecimalField()),
                    igssPorcentaje__in = Subquery(igss.values('porcentaje')),
                        multiplicacionIgss = ExpressionWrapper(F('salarioDevengado') * 
                            F('igssPorcentaje__in'),output_field=DecimalField(decimal_places=2)),
                    isrPorcentaje__in = Subquery(isr.values('porcentaje')),
                    isrMonto__in = Subquery(isr.values('monto_minimo')),
                         calculoIsr = ExpressionWrapper((F('detalle_puesto__monto_salario')+F('bonificacion__in')-(F('isrMonto__in')/12)
                            -F('multiplicacionIgss'))*F('isrPorcentaje__in'),output_field=DecimalField(decimal_places=2)),
                            isrTotal = Case(
                                When(calculoIsr__lte = 0, then=0),
                                When(calculoIsr__gt = 0, then=F('calculoIsr'))
                            ),
                    totalDeuda=Coalesce(Subquery(totalDeudas.values('montoDeudas')), V(0), output_field=FloatField()),
                    totalDeducciones = ExpressionWrapper(F('multiplicacionIgss')+F('isrTotal'), output_field=DecimalField()),
                    salarioLiquido = ExpressionWrapper(F('devengadoTotal')-F('totalDeducciones'), output_field=DecimalField()),
                    )\
        .values('id','first_name','last_name', 'puesto__nombre', 'puesto__departamento__nombre', 'detalle_puesto__jornada',
                'detalle_puesto__monto_salario', 'totalDias', 'horasDia', 'salarioDevengado', 'cantidadHorasE',
                'ingreso__valor_horas_extra', 'horasExtra', 'ingreso__incentivo','incentivo', 'devengadoTotal','multiplicacionIgss',
                'isrTotal', 'totalDeuda', 'totalDeducciones', 'salarioLiquido')

    return JsonResponse({'data':list(listadoUser1)})


def saveDetallePlanilla(request):

    bonIncentivo = Bases_ley.objects.filter(estado=True)[:1]
    igss = Impuesto.objects.filter(estado=True,descripcion__icontains='igss')
    isr = Impuesto.objects.filter(estado=True, descripcion__icontains='isr')
   
    today = datetime.date.today()
    dataMes = monthrange(today.year, mes)
    diasMes = dataMes[1]
    print(mes)
    
    bonIncentivo = Bases_ley.objects.filter(estado=True)
    igss = Impuesto.objects.filter(estado=True,descripcion__icontains='igss')
    isr = Impuesto.objects.filter(estado=True, descripcion__icontains='isr')

    deudas = Pago_movimiento.objects.filter(fecha__month=mes, fecha__year = today.year, estado=True, movimiento__user = OuterRef('pk')).order_by().values('movimiento__user')

    totalDeudas = deudas.annotate(montoDeudas=Coalesce(Sum(F('monto') ), V(0), output_field=FloatField())).values('montoDeudas')

    data = User.objects.filter(ingreso__planilla=True,detalle_puesto__estado=True)\
        .prefetch_related('puesto', 'movimiento')\
        .annotate(diasCompletos = Count('detalle_reloj__fecha', filter=Q(detalle_reloj__fecha__month = mes, detalle_reloj__fecha__year = today.year, 
                        detalle_reloj__horasTrabajadas__gte = F('detalle_puesto__jornada'))),
                            diasPermiso = Count('detalle_reloj__fecha', filter=Q(detalle_reloj__fecha__month = mes, detalle_reloj__fecha__year = today.year,
                                detalle_reloj__diaConPermiso = True)),
                    totalDias = Coalesce(F('diasCompletos') + F('diasPermiso'), V(0), output_field=DecimalField()),
                    horasDia = Sum('detalle_reloj__horasTrabajadas', filter=Q(detalle_reloj__fecha__month = mes, detalle_reloj__fecha__year = today.year, 
                        detalle_reloj__sePaga = True)),
                    pagoHoras = Coalesce(F('detalle_puesto__monto_salario')/diasMes/F('detalle_puesto__jornada')*F('horasDia'), V(0), output_field=DecimalField()),
                    salarioDevengado = ExpressionWrapper( (F('detalle_puesto__monto_salario')/diasMes * F('totalDias')) + F('pagoHoras'), output_field=DecimalField()),
                    counterHorasE = Sum('detalle_reloj__horasExtra', filter=Q(detalle_reloj__fecha__month = mes, detalle_reloj__fecha__year = today.year)),
                        cantidadHorasE = Case(
                        When(Q(ingreso__cantidad_horas_aut= 0) | Q(counterHorasE = None), then=0),
                        When(counterHorasE__gt = F('ingreso__cantidad_horas_aut'), then=F('ingreso__cantidad_horas_aut')),
                        When(counterHorasE__lte = F('ingreso__cantidad_horas_aut'), then=F('counterHorasE'))
                        ),
                            horasExtra = Case(
                                When(ingreso__aplica_hora_extra = False, then=0),
                                When(ingreso__aplica_hora_extra = True, then=ExpressionWrapper(( F('detalle_puesto__monto_salario')/diasMes) /F('detalle_puesto__jornada')
                                * F('ingreso__valor_horas_extra')*F('cantidadHorasE'),output_field=DecimalField()))
                            ),
                    bonificacion__in=Subquery(bonIncentivo.values('bonificacion_incentivo')),
                        incentivo = ExpressionWrapper( F('bonificacion__in') / diasMes * F('diasCompletos'), output_field=DecimalField()),
                    devengadoTotal = ExpressionWrapper(F('salarioDevengado')+F('ingreso__incentivo')+F('incentivo')+
                        F('horasExtra'), output_field=DecimalField()),
                    igssPorcentaje__in = Subquery(igss.values('porcentaje')),
                        multiplicacionIgss = ExpressionWrapper(F('salarioDevengado') * 
                            F('igssPorcentaje__in'),output_field=DecimalField(decimal_places=2)),
                    isrPorcentaje__in = Subquery(isr.values('porcentaje')),
                    isrMonto__in = Subquery(isr.values('monto_minimo')),
                         calculoIsr = ExpressionWrapper((F('detalle_puesto__monto_salario')+F('bonificacion__in')-(F('isrMonto__in')/12)
                            -F('multiplicacionIgss'))*F('isrPorcentaje__in'),output_field=DecimalField(decimal_places=2)),
                            isrTotal = Case(
                                When(calculoIsr__lte = 0, then=0),
                                When(calculoIsr__gt = 0, then=F('calculoIsr'))
                            ),
                    totalDeuda=Coalesce(Subquery(totalDeudas.values('montoDeudas')), V(0), output_field=FloatField()),
                    totalDeducciones = ExpressionWrapper(F('multiplicacionIgss')+F('isrTotal'), output_field=DecimalField()),
                    salarioLiquido = ExpressionWrapper(F('devengadoTotal')-F('totalDeducciones'), output_field=DecimalField()),
                    )\
        .values('id','first_name','last_name', 'puesto__nombre', 'puesto__departamento__nombre', 'detalle_puesto__jornada',
                'detalle_puesto__monto_salario', 'totalDias', 'horasDia', 'salarioDevengado', 'cantidadHorasE',
                'ingreso__valor_horas_extra', 'horasExtra', 'ingreso__incentivo','incentivo', 'devengadoTotal','multiplicacionIgss',
                'isrTotal', 'totalDeuda', 'totalDeducciones', 'salarioLiquido')
    
    for i in range(len(data)):
        detalle = Detalle_planilla(salario_ordinario = data[i]['detalle_puesto__monto_salario'], incentivo = data[i]['bonificacion__in'],\
            bonificaciones = data[i]['ingreso__incentivo'], horas = data[i]['horasExtra'], valor_horas = data[i]['ingreso__valor_horas_extra'],\
            devengadoTotal = data[i]['devengadoTotal'], cuotaIgss = data[i]['multiplicacionIgss'], descuentoIsr = data[i]['isrTotal'],\
            totalDeducciones = data[i]['totalDeducciones'], liquido = data[i]['salarioLiquido'], fechaCreacion = today)
        detalle.bases_ley_id = data[i]['basesLeyId__in']
        detalle.user_id = data[i]['id']
        detalle.save()


    return HttpResponseRedirect(reverse_lazy('planilla:PlanillaList'))


def PlanillaList(request):
    return render(request,'detalle_planilla/detalle_planilla_list.html')

def PlanillaGet(request):    
    planilla = Detalle_planilla.objects.all()\
    .prefetch_related('User').annotate(name=Concat('user__first_name',V(' '),'user__last_name') ).values('id','salario_ordinario','incentivo', 'bonificaciones', 
                    'horas', 'valor_horas', 'devengadoTotal', 'cuotaIgss', 'descuentoIsr', 'totalDeducciones', 'liquido', 'fechaCreacion', 'name')
    return JsonResponse({'data':list(planilla)})





#Movimientos

class MovimientoCreate(CreateView):
    model = Movimiento
    form_class = MovimientoForm
    template_name = 'movimiento/movimiento_form.html'
    success_url = reverse_lazy('planilla:PlanillaList')