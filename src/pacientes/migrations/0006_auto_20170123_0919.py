# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-01-23 12:19
from __future__ import unicode_literals

from django.db import migrations


def set_default_cobertura(apps, schema_editor):
    Paciente = apps.get_model('pacientes', 'Paciente')
    particular = apps.get_model('coberturas_medicas', 'Cobertura').objects.get(cobertura_propia=True)
    Paciente.objects.filter(cobertura_medica__isnull=True).update(cobertura_medica=particular)


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0005_auto_20170122_1428'),
        ('coberturas_medicas', '0004_cobertura_cobertura_propia')
    ]

    operations = [
        migrations.RunPython(set_default_cobertura, migrations.RunPython.noop)
    ]