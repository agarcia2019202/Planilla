# Generated by Django 2.2.1 on 2021-10-29 22:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('planilla', '0042_auto_20211029_1458'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detalle_reloj',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='detalle_reloj', to=settings.AUTH_USER_MODEL),
        ),
    ]
