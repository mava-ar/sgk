# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-03-25 22:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tratamientos', '0006_auto_20170201_1554'),
    ]

    operations = [
        migrations.AddField(
            model_name='planificacion',
            name='motivo_finalizacion',
            field=models.TextField(blank=True, null=True, verbose_name='motivo de finalización'),
        ),
    ]