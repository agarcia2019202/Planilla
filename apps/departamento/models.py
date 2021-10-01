from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# class Departamento(models.Model):
#     nombre = models.CharField(max_length=50)
#     descripcion = models.CharField(max_length=60)

# class Reloj (models.Model):
#     fecha = models.DateTimeField()
#     user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)