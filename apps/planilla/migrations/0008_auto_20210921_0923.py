# Generated by Django 2.2.1 on 2021-09-21 15:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('planilla', '0007_auto_20210920_0827'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingreso',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='movimiento',
            name='descripcion',
            field=models.CharField(max_length=150),
        ),
    ]
