# Generated by Django 2.2.1 on 2021-09-14 18:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('departamento', '0003_reloj'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Departamento',
        ),
        migrations.DeleteModel(
            name='Reloj',
        ),
    ]
