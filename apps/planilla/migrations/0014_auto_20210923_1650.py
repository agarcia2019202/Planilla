# Generated by Django 2.2.1 on 2021-09-23 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planilla', '0013_ingreso_monto_salario'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingreso',
            name='monto_salario',
        ),
        migrations.AlterField(
            model_name='ingreso',
            name='cantidad_horas_aut',
            field=models.PositiveIntegerField(),
        ),
    ]