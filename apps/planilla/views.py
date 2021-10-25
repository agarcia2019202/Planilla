# import datetime
# from django.db.models import Sum
# from django.db.models.aggregates import Count
# from django.db.models.functions import Concat
# from django.db.models import DecimalField, F, ExpressionWrapper, Value, Subquery
# from django.db.models.expressions import Case, When
# from django.db.models.query_utils import Q
# from apps.planilla.models import *
# from apps.planilla.forms import *
# from django.http.response import JsonResponse
# from django.shortcuts import render, redirect
# from django.views.generic import CreateView
# from django.urls import reverse_lazy
# from django.http import HttpResponse, HttpResponseRedirect, Http404
# from calendar import monthrange

# #Cambios
# """
# - Validar que sea un mes valido (frontend-backend)
# - Cuadrar planilla

# """



# #Detalle Planilla
# def PlanillaPreList(request):
#     #Enviar formulario (input, img, button)    
#     return render(request,'detalle_planilla/planilla_prelist.html')


# def DetallePlanilla(request):
#     """
#     #Querys de validacion
#     hora = Horas.objects.get(user=request.user) -->nueva tabla (aggregate para sumar horas)
#     hora.suma = 8

#     if hora.suma>horasExtra:
#         hora =hora.suma
#     else:
#         hora = horasExtra
#     """
    
    
#     # horasExtra = Subquery() #tabla horas extra 15
#     try:
#         Bases_ley.objects.get(~Q(bonificacion_incentivo__lte=0), estado=True)
#     except Bases_ley.DoesNotExist:
#         print('COMUNIQUESE CON EL ADMINISTRADOR, NO HAY BASES DE LEY')
#         raise Http404
#     try:
#         Impuesto.objects.get(estado=True, descripcion__icontains = 'igss')
#     except Impuesto.DoesNotExist:
#         print('COMUNIQUESE CON EL ADMINISTRADOR, NO HAY IGSS REGISTRADO')
#         raise Http404
#     try:
#         Impuesto.objects.get(estado=True, descripcion__icontains = 'isr')
#     except Impuesto.DoesNotExist:
#         print('COMUNIQUESE CON EL ADMINISTRADOR, NO HAY ISR REGISTRADO')
#         raise Http404

#     getMes = request.POST['mes']
#     mes = int(getMes)    
#     today = datetime.date.today()
#     dataMes = monthrange(today.year, mes)
#     diasMes = dataMes[1]
    
#     bonIncentivo = Bases_ley.objects.filter(estado=True)
#     igss = Impuesto.objects.filter(estado=True,descripcion__icontains='igss')
#     isr = Impuesto.objects.filter(estado=True, descripcion__icontains='isr')
#     #lo de poder seleccionar el mes(Septiembre)
#     deudas = Pago_movimiento.objects.select_related('movimiento').filter(fecha__month=mes, movimiento__user = 4).aggregate(suma=Sum('monto'))
#     print(deudas)

#     #, movimiento__fecha_finalizacion__gte = today
#     listadoUser1 = User.objects.filter(ingreso__planilla=True,detalle_puesto__estado=True)\
#         .prefetch_related('puesto', 'movimiento', 'pago_movimiento')\
#         .annotate(diasTrabajados = Count('reloj__fecha', filter=Q(reloj__fecha__month = mes, reloj__fecha__year = today.year)),
#                     salarioDevengado = ExpressionWrapper( F('detalle_puesto__monto_salario')/diasMes * F('diasTrabajados'), output_field=DecimalField()),
#                     horasExtra = Case(
#                         When(ingreso__aplica_hora_extra = False, then=0),
#                         When(ingreso__aplica_hora_extra = True, then=ExpressionWrapper(( F('detalle_puesto__monto_salario')/diasMes) /8 * F('ingreso__valor_horas_extra')*
#                             F('ingreso__cantidad_horas_aut'),output_field=DecimalField(max_digits=9, decimal_places=2)))
#                         ),
#                     bonificacion__in=Subquery(bonIncentivo.values('bonificacion_incentivo')),
#                         incentivo = ExpressionWrapper( F('bonificacion__in') / diasMes * F('diasTrabajados'), output_field=DecimalField()),
#                     devengadoTotal = ExpressionWrapper(F('salarioDevengado')+F('ingreso__incentivo')+F('incentivo')+
#                         F('horasExtra'), output_field=DecimalField()),
#                     igssPorcentaje__in = Subquery(igss.values('porcentaje')),
#                         multiplicacionIgss = ExpressionWrapper(F('salarioDevengado') * 
#                             F('igssPorcentaje__in'),output_field=DecimalField(decimal_places=2)),
#                     isrPorcentaje__in = Subquery(isr.values('porcentaje')),
#                     isrMonto__in = Subquery(isr.values('monto_minimo')),
#                          calculoIsr = ExpressionWrapper((F('detalle_puesto__monto_salario')+F('bonificacion__in')-(F('isrMonto__in')/12)
#                             -F('multiplicacionIgss'))*F('isrPorcentaje__in'),output_field=DecimalField(decimal_places=2)),
#                             isrTotal = Case(
#                                 When(calculoIsr__lte = 0, then=0),
#                                 When(calculoIsr__gt = 0, then=F('calculoIsr'))
#                             ),
#                     deudas = Sum('movimiento__pago_movimiento__monto'),
#                     totalDeducciones = ExpressionWrapper(F('multiplicacionIgss')+F('isrTotal'), output_field=DecimalField()),
#                     salarioLiquido = ExpressionWrapper(F('devengadoTotal')-F('totalDeducciones'), output_field=DecimalField()),
#                     )\
#         .values('id','first_name','last_name', 'puesto__nombre', 'puesto__departamento__nombre', 'detalle_puesto__monto_salario', 
#                 'diasTrabajados', 'salarioDevengado', 'ingreso__cantidad_horas_aut', 'ingreso__valor_horas_extra', 'horasExtra', 'ingreso__incentivo','incentivo',
#                 'devengadoTotal','multiplicacionIgss', 'isrTotal', 'deudas', 'totalDeducciones', 'salarioLiquido')

#     return JsonResponse({'data':list(listadoUser1)})


# def saveDetallePlanilla(request):

#     today = datetime.date.today()
#     bonIncentivo = Bases_ley.objects.filter(estado=True)[:1]
#     igss = Impuesto.objects.filter(estado=True,descripcion__icontains='igss')
#     isr = Impuesto.objects.filter(estado=True, descripcion__icontains='isr')

#     data = User.objects.filter(ingreso__planilla=True,detalle_puesto__estado=True)\
#         .prefetch_related('Puesto')\
#         .annotate(horasExtra = Case(
#                         When(ingreso__aplica_hora_extra = False, then=0),
#                         When(ingreso__aplica_hora_extra = True, then=ExpressionWrapper((F('detalle_puesto__monto_salario')/30)/8*F('ingreso__valor_horas_extra')*
#                             F('ingreso__cantidad_horas_aut'),output_field=DecimalField(max_digits=9, decimal_places=2)))
#                         ),
#                     bonificacion__in=Subquery(bonIncentivo.values('bonificacion_incentivo')),
#                     basesLeyId__in = Subquery(bonIncentivo.values('id')),
#                     devengadoTotal = ExpressionWrapper(F('detalle_puesto__monto_salario')+F('ingreso__incentivo')+F('bonificacion__in')+
#                         F('horasExtra'), output_field=DecimalField()),
#                     igssPorcentaje__in = Subquery(igss.values('porcentaje')),
#                         multiplicacionIgss = ExpressionWrapper(F('detalle_puesto__monto_salario') * 
#                             F('igssPorcentaje__in'),output_field=DecimalField(decimal_places=2)),
#                     isrPorcentaje__in = Subquery(isr.values('porcentaje')),
#                     isrMonto__in = Subquery(isr.values('monto_minimo')),
#                          calculoIsr = ExpressionWrapper((F('detalle_puesto__monto_salario')+F('bonificacion__in')-(F('isrMonto__in')/12)
#                             -F('multiplicacionIgss'))*F('isrPorcentaje__in'),output_field=DecimalField(decimal_places=2)),
#                             isrTotal = Case(
#                                 When(calculoIsr__lte = 0, then=0),
#                                 When(calculoIsr__gt = 0, then=F('calculoIsr'))
#                             ),
#                     totalDeducciones = ExpressionWrapper(F('multiplicacionIgss')+F('isrTotal'), output_field=DecimalField()),
#                     salarioLiquido = ExpressionWrapper(F('devengadoTotal')-F('totalDeducciones'), output_field=DecimalField()),
#                      )\
#         .values('id','first_name','last_name', 'puesto__nombre', 'detalle_puesto__monto_salario', 'ingreso__incentivo', 
#                 'ingreso__valor_horas_extra', 'horasExtra', 'bonificacion__in', 'devengadoTotal','multiplicacionIgss',
#                 'isrTotal', 'totalDeducciones', 'salarioLiquido', 'basesLeyId__in')
    
#     for i in range(len(data)):
#         detalle = Detalle_planilla(salario_ordinario = data[i]['detalle_puesto__monto_salario'], incentivo = data[i]['bonificacion__in'],\
#             bonificaciones = data[i]['ingreso__incentivo'], horas = data[i]['horasExtra'], valor_horas = data[i]['ingreso__valor_horas_extra'],\
#             devengadoTotal = data[i]['devengadoTotal'], cuotaIgss = data[i]['multiplicacionIgss'], descuentoIsr = data[i]['isrTotal'],\
#             totalDeducciones = data[i]['totalDeducciones'], liquido = data[i]['salarioLiquido'], fechaCreacion = today)
#         detalle.bases_ley_id = data[i]['basesLeyId__in']
#         detalle.user_id = data[i]['id']
#         detalle.save()


#     return HttpResponseRedirect(reverse_lazy('planilla:PlanillaList'))


# def PlanillaList(request):
#     return render(request,'detalle_planilla/detalle_planilla_list.html')

# def PlanillaGet(request):    
#     planilla = Detalle_planilla.objects.all()\
#     .prefetch_related('User').annotate(name=Concat('user__first_name',Value(' '),'user__last_name') ).values('id','salario_ordinario','incentivo', 'bonificaciones', 
#                     'horas', 'valor_horas', 'devengadoTotal', 'cuotaIgss', 'descuentoIsr', 'totalDeducciones', 'liquido', 'fechaCreacion', 'name')
#     return JsonResponse({'data':list(planilla)})





# #Movimientos

# class MovimientoCreate(CreateView):
#     model = Movimiento
#     form_class = MovimientoForm
#     template_name = 'movimiento/movimiento_form.html'
#     success_url = reverse_lazy('planilla:PlanillaList')