# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-04-11 17:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tratamientos', '0010_auto_20170411_1425'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sesion',
            name='motivo_consulta',
        ),
    ]
