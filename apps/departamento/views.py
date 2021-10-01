# from django.http.response import JsonResponse
# from apps.departamento.departamento_form import DepartamentoForm
# from django.shortcuts import render, redirect
# from apps.departamento.models import Departamento
# from django.views.generic import CreateView, ListView, TemplateView, UpdateView
# from django.urls import reverse_lazy
# from django.http import HttpResponse, HttpResponseRedirect
# import json


# class DepartamentoCreate(CreateView):
#     model = Departamento
#     form_class = DepartamentoForm
#     template_name = 'departamento/departamento_form.html'
#     success_url = reverse_lazy('departamento:DepartamentoList')

# #Mostramos la template
# def DepartamentoList(request):
#     return render(request,'departamento/departamento_list.html')

# #Filtramos y serializamos los datos
# def DepartamentoListado(request):    
#     departamento = Departamento.objects.all().values('pk','nombre','descripcion')    
#     return JsonResponse({'data':list(departamento)})

# class DepartamentoUpdate(UpdateView):
#     model = Departamento
#     form_class = DepartamentoForm
#     template_name = 'departamento/departamento_form.html'
#     success_url = reverse_lazy('departamento:DepartamentoList')

#     def post(self, request, *args, **kwargs):
        
#         self.object = self.get_object
#         id_estado = kwargs['pk']
#         solicitud = self.model.objects.get(id=id_estado)
#         form = self.form_class(request.POST, instance=solicitud)
#         if form.is_valid() and not self.request.is_ajax():
#             form.save()
#             return HttpResponseRedirect(self.get_success_url())
#         else:
#             return self.render_to_response(self.get_context_data(form=form))


# # class DepartamentoUpdate(UpdateView):
# #     model = Departamento
# #     form_class = DepartamentoForm
# #     template_name = 'departamento/departamento_form.html'
# #     success_url = reverse_lazy('departamento:departamento_list')
    
    
#     # Manera de Angel ---> Optima para cantidades masivas (Ajax - Datatables(Modificado))
#     # Manera Cliente --> (Ajax - Datatables)
    
    
    
    
    