# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-04-11 17:25
from __future__ import unicode_literals

from django.db import migrations


def asociar_sesion_con_planificacion(apps, schema_editor):
    Sesion = apps.get_model("tratamientos", "Sesion")
    sesiones = Sesion.objects.filter(motivo_consulta__isnull=False)
    for sesion in sesiones:
        planificacion = sesion.motivo_consulta.planificaciones.filter(
            creado_el__lte=sesion.fecha).order_by('-creado_el').first()
        sesion.planificacion = planificacion
        sesion.motivo_consulta = None
        sesion.save()


class Migration(migrations.Migration):

    dependencies = [
        ('tratamientos', '0009_sesion_planificacion'),
    ]

    operations = [
        migrations.RunPython(asociar_sesion_con_planificacion, migrations.RunPython.noop)
    ]