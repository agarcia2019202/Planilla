# Generated by Django 2.2.1 on 2021-10-30 02:38

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planilla', '0043_auto_20211029_1650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingreso',
            name='cantidad_horas_aut',
            field=models.DecimalField(decimal_places=2, max_digits=9, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name='cantidad_horas_aut'),
        ),
    ]
