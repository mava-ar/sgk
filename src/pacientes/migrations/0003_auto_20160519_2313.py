# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-20 02:13
from __future__ import unicode_literals

import dj_utils.mixins
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20160508_1757'),
        ('pacientes', '0002_auto_20160519_2312'),
    ]

    operations = [
        migrations.CreateModel(
            name='EntradaHistoriaClinica',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creado_el', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('modificado_el', models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')),
            ],
            options={
                'verbose_name': 'Entrada de historia clínica',
                'verbose_name_plural': 'Entradas de historia clínica',
            },
            bases=(models.Model, dj_utils.mixins.ShowInfoMixin),
        ),
        migrations.CreateModel(
            name='ComentariosHistoriaClinica',
            fields=[
                ('entradahistoriaclinica_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='pacientes.EntradaHistoriaClinica')),
                ('comentarios', models.TextField(verbose_name='comentarios')),
            ],
            options={
                'verbose_name': 'comentario de historia clinica',
                'verbose_name_plural': 'comentarios de historia clinica',
            },
            bases=('pacientes.entradahistoriaclinica',),
        ),
        migrations.CreateModel(
            name='ImagenesHistoriaClinica',
            fields=[
                ('entradahistoriaclinica_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='pacientes.EntradaHistoriaClinica')),
                ('imagen', models.ImageField(upload_to='historia_imagenes', verbose_name='imágen')),
                ('comentarios', models.TextField(blank=True, null=True, verbose_name='comentarios')),
            ],
            options={
                'verbose_name': 'imagen de historia clínica',
                'verbose_name_plural': 'imágenes de historia clínica',
            },
            bases=('pacientes.entradahistoriaclinica',),
        ),
        migrations.AddField(
            model_name='entradahistoriaclinica',
            name='paciente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entradas_historiaclinica', to='pacientes.Paciente'),
        ),
        migrations.AddField(
            model_name='entradahistoriaclinica',
            name='profesional',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Profesional'),
        ),
    ]