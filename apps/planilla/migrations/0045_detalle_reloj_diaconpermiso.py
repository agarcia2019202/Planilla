# Generated by Django 2.2.1 on 2021-11-16 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planilla', '0044_auto_20211029_2038'),
    ]

    operations = [
        migrations.AddField(
            model_name='detalle_reloj',
            name='diaConPermiso',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
