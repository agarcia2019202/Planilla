# Generated by Django 2.2.1 on 2021-10-19 21:31

from decimal import Decimal
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('planilla', '0039_delete_ingreso'),
    ]

    operations = [
        migrations.AddField(
            model_name='detalle_puesto',
            name='jornada',
            field=models.PositiveIntegerField(default=8),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='impuesto',
            name='monto_minimo',
            field=models.DecimalField(decimal_places=2, max_digits=8, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))], verbose_name='monto_minimo'),
        ),
        migrations.AlterField(
            model_name='interes',
            name='mora',
            field=models.DecimalField(decimal_places=3, max_digits=9, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name='mora'),
        ),
        migrations.CreateModel(
            name='Ingreso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('incentivo', models.DecimalField(decimal_places=2, max_digits=8, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name='incentivo')),
                ('aplica_hora_extra', models.BooleanField()),
                ('cantidad_horas_aut', models.PositiveIntegerField()),
                ('valor_horas_extra', models.DecimalField(decimal_places=2, max_digits=8, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name='valor_horas_extra')),
                ('planilla', models.BooleanField()),
                ('honorarios', models.BooleanField()),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
