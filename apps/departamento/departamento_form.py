# from django import forms
# from django.forms import widgets
# from apps.departamento.models import Departamento

# class DepartamentoForm(forms.ModelForm):
#     class Meta:
#         model = Departamento

#         fields = [
#             'nombre',
#             'descripcion',
#         ]
#         labels = {
#             'nombre': 'Nombre',
#             'descripcion': 'Descripción',
#         }
#         widgets = {
#             'nombre': forms.TextInput(attrs={'class':'form-control'}),
#             'descripcion': forms.TextInput(attrs={'class':'form-control'}),
#         }