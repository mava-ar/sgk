# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-01-23 11:23
from __future__ import unicode_literals

from django.db import migrations, models


def generate_particular_cobertura(apps, schema_editor):
    Cobertura = apps.get_model('coberturas_medicas', 'Cobertura')
    Cobertura.objects.update(cobertura_propia=False)
    particular, _ = Cobertura.objects.get_or_create(nombre='Particular')
    particular.cobertura_propia = True
    particular.save()


class Migration(migrations.Migration):

    dependencies = [
        ('coberturas_medicas', '0003_auto_20160525_2139'),
    ]

    operations = [
        migrations.AddField(
            model_name='cobertura',
            name='cobertura_propia',
            field=models.BooleanField(default=False, help_text='No es una cobertura, sino el pago del servicio por el particular', verbose_name='cobertura propia'),
        ),
        migrations.RunPython(generate_particular_cobertura, migrations.RunPython.noop)
    ]
