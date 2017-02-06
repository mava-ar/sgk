# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-02-01 18:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


def asociar_sesiones_con_profesional(apps, schema_editor):
    Profesional = apps.get_model('core', 'Profesional')
    Sesion = apps.get_model('tratamientos', 'Sesion')
    try:
        a_pro = Profesional.objects.get(pk=1)
        Sesion.objects.update(profesional=a_pro)
    except Profesional.DoesNotExist:
        # si no hay profesional, es una migraciones inicial
        Sesion.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20170129_1529'),
        ('tratamientos', '0004_auto_20170201_0958'),
    ]

    operations = [
        migrations.AddField(
            model_name='sesion',
            name='profesional',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sesiones', to='core.Profesional'),
        ),
        migrations.RunPython(asociar_sesiones_con_profesional, migrations.RunPython.noop)
    ]