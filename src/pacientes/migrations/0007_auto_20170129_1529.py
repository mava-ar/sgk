# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-01-29 18:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0006_auto_20170123_0919'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='paciente',
            options={'ordering': ('persona',), 'verbose_name': 'paciente', 'verbose_name_plural': 'pacientes'},
        ),
    ]