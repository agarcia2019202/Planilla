# Generated by Django 2.2.1 on 2021-10-25 18:04

from decimal import Decimal
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('planilla', '0040_auto_20211019_1531'),
    ]

    operations = [
        migrations.AddField(
            model_name='reloj',
            name='horasExtra',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reloj',
            name='permiso',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Detalle_reloj',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('calculo', models.DecimalField(decimal_places=2, max_digits=9, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name='calculo')),
                ('horasTrabajadas', models.DecimalField(decimal_places=2, max_digits=9, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))], verbose_name='horasTrabajadas')),
                ('horasExtra', models.DecimalField(decimal_places=2, max_digits=9, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name='horasExtra')),
                ('permisos', models.DecimalField(decimal_places=2, max_digits=9, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name='permisos')),
                ('sePaga', models.BooleanField()),
                ('nota', models.CharField(max_length=150)),
                ('autorizo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='autorizador', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='usuario', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
