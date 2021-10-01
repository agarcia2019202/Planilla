from django.utils.functional import cached_property
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.db.models.base import Model
from django.db.models import CharField, DecimalField
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal
# Create your models here.

class Departamento(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=80)

    def __str__(self):
        return '{}'.format(self.nombre)

class Puesto(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100)
    estado = models.BooleanField()
    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True)
    user = models.ManyToManyField(User, through='Detalle_puesto')

    def __str__(self):
        return '{}'.format(self.nombre)

class Detalle_puesto(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    puesto = models.ForeignKey(Puesto, on_delete=models.SET_NULL, null=True)
    monto_salario = models.DecimalField(_(u'monto_salario'), decimal_places=2, max_digits=12,validators=[MinValueValidator(Decimal('0.01'))], null=False, blank=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    minimo = models.BooleanField()
    estado = models.BooleanField()

class Reloj(models.Model):
    fecha = models.DateTimeField()
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)

class Ingreso(models.Model):
    incentivo = models.DecimalField(_(u'incentivo'), decimal_places=2, max_digits=8,validators=[MinValueValidator(Decimal('0.00'))], null=True, blank=True)  
    aplica_hora_extra = models.BooleanField()
    cantidad_horas_aut = models.PositiveIntegerField()
    valor_horas_extra = models.DecimalField(_(u'valor_horas_extra'), decimal_places=2, max_digits=8,validators=[MinValueValidator(Decimal('0.00'))], null=True, blank=True)
    planilla = models.BooleanField()
    honorarios = models.BooleanField()
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)

    #manipular nadie 
#    def save(self, *args, **kwargs):
 #       puesto= Puesto.objects.
  #      detallePuesto = Detalle_puesto.objects.create(user=self.user,puesto=)

    # angel 6700 programdor fehca(hoyu)
    # angel 2500 jefe programacion  fecha(hoy +365 )
    # angel 6700 gerente fecha(hoy + 7000)
class Tipo_movimiento(models.Model):
    codigo = models.CharField(max_length=40)
    descripcion = models.CharField(max_length=80)
    estado = models.BooleanField()

    def __str__(self):
        return f'{self.codigo} - {self.descripcion}'

class Interes(models.Model):
    descripcion = models.CharField(max_length=150)
    porcentaje = models.DecimalField(_(u'porcentaje'), decimal_places=4, max_digits=7,validators=[MinValueValidator(Decimal('0.01'))], null=False, blank=False)
    mora = models.DecimalField(_(u'mora'), decimal_places=3, max_digits=9,validators=[MinValueValidator(Decimal('0.00'))], null=True, blank=True)
    max_pagos = models.PositiveIntegerField()
    estado = models.BooleanField()

    def __str__(self):
        return f'{self.porcentaje*100}% - {self.max_pagos} pagos'

class Movimiento(models.Model):
    descripcion = models.CharField(max_length=150)
    monto = models.DecimalField(_(u'monto'), decimal_places=2, max_digits=9,validators=[MinValueValidator(Decimal('0.01'))], null=False, blank=False)
    fecha_creacion = models.DateField()
    fecha_finalizacion = models.DateField()
    no_pagos = models.PositiveIntegerField()
    fin_mes = models.BooleanField(default=False)
    tipo_movimiento = models.ForeignKey(Tipo_movimiento, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    interes = models.ForeignKey(Interes, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.descripcion}'

class Pago_movimiento(models.Model):
    fecha = models.DateField()
    monto = models.DecimalField(_(u'monto'), decimal_places=2, max_digits=9,validators=[MinValueValidator(Decimal('0.01'))], null=False, blank=False)
    estado = models.BooleanField()
    movimiento = models.ForeignKey(Movimiento, on_delete=models.SET_NULL, null=True)

class Impuesto(models.Model):
    descripcion = models.CharField(max_length=60)
    porcentaje = models.DecimalField(_(u'porcentaje'), decimal_places=4, max_digits=7,validators=[MinValueValidator(Decimal('0.01'))])
    monto_minimo = models.DecimalField(_(u'monto_minimo'), decimal_places=2, max_digits=8,validators=[MinValueValidator(Decimal('0.01'))], null=True, blank=True)
    estado = models.BooleanField()

class Bases_ley(models.Model):
    fecha = models.DateField()
    salario_minimo = models.DecimalField(_(u'salario_minimo'), decimal_places=2, max_digits=9,validators=[MinValueValidator(Decimal('0.01'))], null=False, blank=False)
    bonificacion_incentivo = models.DecimalField(_(u'bonificacion_incentivo'), decimal_places=2, max_digits=6,validators=[MinValueValidator(Decimal('0.01'))], null=False, blank=False)
    estado = models.BooleanField()
    impuesto = models.ManyToManyField(Impuesto, through='Detalle_impuesto')

    def __str__(self):
        return f'{self.fecha}'

class Detalle_impuesto(models.Model):
    impuesto = models.ForeignKey(Impuesto, on_delete=models.SET_NULL, null=True)
    bases_ley = models.ForeignKey(Bases_ley, on_delete=models.SET_NULL, null=True)

class Detalle_planilla(models.Model):
    salario_ordinario = models.DecimalField(max_digits=9, decimal_places=2)
    dias_trabajados = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    incentivo = models.DecimalField(max_digits=5, decimal_places=2)
    bonificaciones = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    productividad = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    horas = models.DecimalField(max_digits=8, decimal_places=2)
    valor_horas = models.DecimalField(max_digits=5, decimal_places=2)
    salarioTotal = models.DecimalField(max_digits=8, decimal_places=2)
    cuotaIgss = models.DecimalField(max_digits=8, decimal_places=2)
    descuentoIsr = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    totalDeducciones = models.DecimalField(max_digits=8, decimal_places=2)
    liquido = models.DecimalField(max_digits=8, decimal_places=2)
    fechaCreacion = models.DateField()
    bases_ley = models.ForeignKey(Bases_ley, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
