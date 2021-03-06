# Generated by Django 2.2.1 on 2021-09-27 14:22

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planilla', '0017_auto_20210927_0820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='impuesto',
            name='monto_minimo',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))], verbose_name='monto_minimo'),
        ),
    ]
