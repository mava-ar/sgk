# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-01-26 00:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_delete_profesion'),
    ]

    operations = [
        migrations.AddField(
            model_name='contacto',
            name='notificar_sms',
            field=models.BooleanField(default=True, verbose_name='notificar por SMS'),
        ),
    ]
