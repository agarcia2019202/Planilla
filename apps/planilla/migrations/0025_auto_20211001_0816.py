# Generated by Django 2.2.1 on 2021-10-01 14:16

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planilla', '0024_detalle_planilla'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bases_ley',
            name='bonificacion_incentivo',
            field=models.DecimalField(decimal_places=2, max_digits=6, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))], verbose_name='bonificacion_incentivo'),
        ),
        migrations.AlterField(
            model_name='bases_ley',
            name='salario_minimo',
            field=models.DecimalField(decimal_places=2, max_digits=9, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))], verbose_name='salario_minimo'),
        ),
        migrations.AlterField(
            model_name='ingreso',
            name='incentivo',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name='incentivo'),
        ),
        migrations.AlterField(
            model_name='ingreso',
            name='valor_horas_extra',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name='valor_horas_extra'),
        ),
        migrations.AlterField(
            model_name='interes',
            name='max_pagos',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='interes',
            name='mora',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=9, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name='mora'),
        ),
        migrations.AlterField(
            model_name='interes',
            name='porcentaje',
            field=models.DecimalField(decimal_places=4, max_digits=7, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))], verbose_name='porcentaje'),
        ),
        migrations.AlterField(
            model_name='movimiento',
            name='monto',
            field=models.DecimalField(decimal_places=2, max_digits=9, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))], verbose_name='monto'),
        ),
        migrations.AlterField(
            model_name='movimiento',
            name='no_pagos',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='pago_movimiento',
            name='monto',
            field=models.DecimalField(decimal_places=2, max_digits=9, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))], verbose_name='monto'),
        ),
    ]
