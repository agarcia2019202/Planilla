from django import forms
from apps.planilla.models import *

class MovimientoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipo_movimiento'].queryset = Tipo_movimiento.objects.filter(estado = True)
        self.fields['interes'].queryset = Interes.objects.filter(estado = True)

    class Meta:
        model = Movimiento

        fields = [
            'monto',
            'fecha_creacion',
            'fecha_finalizacion',
            'descripcion',
            'fin_mes',
            'tipo_movimiento',
            'interes',
            'user',
        ]
        labels = {
            'monto': 'Monto',
            'fecha_creacion': 'Fecha Inicio',
            'fecha_finalizacion': 'Fecha Fin',
            'descripcion': 'Descripción',
            'fin_mes': 'Pago Fin de Mes',
            'tipo_movimiento': 'Tipo de Movimiento',
            'interes': 'Intereses',
            'user': 'Usuario',
        }
        widgets = {
            'monto': forms.TextInput(attrs={'class':'form-control'}),
            'fecha_creacion': forms.SelectDateWidget(attrs={'class':'form-control'}),
            'fecha_finalizacion': forms.SelectDateWidget(attrs={'class':'form-control'}),
            'descripcion': forms.Textarea(attrs={'class':'form-control'}),
            'fin_mes': forms.CheckboxInput(attrs={'class':'form-control'}),
            'tipo_movimiento': forms.Select(attrs={'class':'form-control'}),
            'interes': forms.Select(attrs={'class':'form-control'}),
            'user': forms.Select(attrs={'class':'form-control'}),
        }


# class DetallePlanillaForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['bases_ley'].queryset = Bases_ley.objects.filter(estado=True)

#     class Meta:
#         model = Detalle_planilla

#         fields = [
#             'salario_ordinario',
#             'dias_trabajados',
#             'incentivo',
#             'bonificaciones',
#             'productividad',
#             'horas',
#             'valor_horas',
#             'devengadoTotal',
#             'cuotaIgss',
#             'descuentoIsr',
#             'totalDeducciones',
#             'liquido',
#             'bases_ley',
#             'user',
#         ]
#         labels = {
#             'salario_ordinario': 'Salario Ordinario',
#             'dias_trabajados': 'Dias Trabajados',
#             'incentivo': 'Incentivo',
#             'bonificaciones': 'Bonificaciones',
#             'productividad': 'Productividad',
#             'horas': 'Horas',
#             'valor_horas': 'Valor Horas',
#             'devengadoTotal': 'Salario Total',
#             'cuotaIgss': 'IGSS',
#             'descuentoIsr': 'ISR',
#             'totalDeducciones': 'Total Deducciones',
#             'liquido': 'Liquido',
#             'bases_ley': 'Bases Ley',
#             'user': 'Usuario',
#         }
#         widgets = {
#             'salario_ordinario': forms.TextInput(attrs={'class':'form-control'}),
#             'dias_trabajados': forms.TextInput(attrs={'class':'form-control'}),
#             'incentivo': forms.TextInput(attrs={'class':'form-control'}),
#             'bonificaciones': forms.TextInput(attrs={'class':'form-control'}),
#             'productividad': forms.TextInput(attrs={'class':'form-control'}),
#             'horas': forms.TextInput(attrs={'class':'form-control'}),
#             'valor_horas': forms.TextInput(attrs={'class':'form-control'}),
#             'devengadoTotal': forms.TextInput(attrs={'class':'form-control'}),
#             'cuotaIgss': forms.TextInput(attrs={'class':'form-control'}),
#             'descuentoIsr': forms.TextInput(attrs={'class':'form-control'}),
#             'totalDeducciones': forms.TextInput(attrs={'class':'form-control'}),
#             'liquido': forms.TextInput(attrs={'class':'form-control'}),
#             'bases_ley': forms.Select(attrs={'class':'form-control'}),
#             'user': forms.Select(attrs={'class':'form-control'}),
#         }