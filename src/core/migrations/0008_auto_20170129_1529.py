# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-01-29 18:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20170127_2031'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='persona',
            options={'ordering': ('nombre', 'apellido'), 'verbose_name': 'persona', 'verbose_name_plural': 'personas'},
        ),
    ]
