# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-08 03:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cobertura',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creado_el', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('modificado_el', models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')),
                ('nombre', models.CharField(max_length=255, verbose_name='nombre')),
                ('codigo', models.CharField(blank=True, max_length=255, verbose_name='código')),
                ('telefono', models.CharField(blank=True, max_length=25, verbose_name='teléfono')),
                ('fax', models.CharField(blank=True, max_length=25, verbose_name='fax')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email')),
                ('activo', models.BooleanField(default=True, verbose_name='activo')),
                ('paga_por_sesion', models.BooleanField(default=False, help_text='Seleccionar para indicar que la cobertura paga cada sesión individualmente.', verbose_name='paga por sesión')),
            ],
            options={
                'verbose_name': 'cobertura médica',
                'verbose_name_plural': 'coberturas médicas',
            },
        ),
        migrations.CreateModel(
            name='RegistroValorPrestacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creado_el', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('modificado_el', models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')),
                ('monto', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='monto ($)')),
                ('fecha_baja', models.DateTimeField(null=True, verbose_name='fecha de baja')),
                ('cobertura', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='valores', to='coberturas_medicas.Cobertura')),
            ],
            options={
                'verbose_name': 'valor de prestación',
                'verbose_name_plural': 'valores de prestación',
            },
        ),
    ]
