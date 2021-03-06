# Generated by Django 2.2.1 on 2021-10-29 20:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('planilla', '0041_auto_20211025_1204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detalle_reloj',
            name='autorizo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='autorizador', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='detalle_reloj',
            name='nota',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
