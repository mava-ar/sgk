# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-08 03:42
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pacientes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MotivoConsulta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creado_el', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('modificado_el', models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')),
                ('motivo_consulta_paciente', models.TextField(blank=True, default='', help_text='Signos y síntomas explicados por el paciente.', verbose_name='motivo según el paciente')),
                ('diagnostico_medico', models.TextField(help_text='Diagnóstico que elaboró el médico especialista.', verbose_name='diagnóstico médico')),
                ('evaluacion_kinesica', models.TextField(help_text='Evaluación elaborada por el kinesiólogo/a.', verbose_name='evaluación kinésica')),
                ('tratamientos_previos', models.TextField(blank=True, help_text='Descripción de tratamientos previos por el mismo motivo de consulta', verbose_name='tratamientos previos')),
                ('observaciones', models.TextField(blank=True, verbose_name='observaciones')),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='motivos_de_consulta', to='pacientes.Paciente', verbose_name='paciente')),
            ],
            options={
                'verbose_name': 'motivo de consulta',
                'verbose_name_plural': 'motivos de consulta',
            },
        ),
        migrations.CreateModel(
            name='Objetivo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creado_el', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('modificado_el', models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')),
                ('descripcion', models.CharField(max_length=255, verbose_name='descripción')),
                ('fecha_inicio', models.DateField(null=True, verbose_name='fecha de inicio')),
                ('fecha_cumplido', models.DateField(null=True, verbose_name='fecha de éxito')),
                ('observaciones', models.TextField(blank=True, verbose_name='observaciones')),
                ('motivo_consulta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='objetivos', to='tratamientos.MotivoConsulta', verbose_name='motivo de consulta')),
            ],
            options={
                'verbose_name': 'objectivo',
                'verbose_name_plural': 'objetivos',
            },
        ),
        migrations.CreateModel(
            name='Planificacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creado_el', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('modificado_el', models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')),
                ('fecha_ingreso', models.DateField(auto_now_add=True, verbose_name='fecha de ingreso')),
                ('fecha_alta', models.DateField(blank=True, help_text='fecha de alta tentativa.', null=True, verbose_name='fecha de alta')),
                ('cantidad_sesiones', models.IntegerField(default=10, help_text='Cantidad de sesiones necesarias recetadas por el médico.', verbose_name='cantidad de sesiones')),
                ('frecuencia', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(7)], verbose_name='frecuencia semanal')),
                ('estado', models.IntegerField(choices=[(1, 'Planificado'), (2, 'En curso'), (3, 'Finalizado'), (4, 'Cancelado')], default=1, verbose_name='estado')),
                ('comentarios', models.TextField(blank=True, null=True, verbose_name='comentarios')),
                ('conclusion', models.TextField(blank=True, null=True, verbose_name='conclusión')),
                ('motivo_consulta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='planificaciones', to='tratamientos.MotivoConsulta')),
            ],
            options={
                'verbose_name': 'planificación',
                'verbose_name_plural': 'planificaciones',
            },
        ),
        migrations.CreateModel(
            name='Sesion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creado_el', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('modificado_el', models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')),
                ('fecha', models.DateField(verbose_name='fecha')),
                ('duracion', models.PositiveSmallIntegerField(default=60, help_text='Duración de la sesión en minutos', verbose_name='duración de la sesión')),
                ('estado_paciente', models.TextField(blank=True, help_text='Descripción de cómo se siente el paciente antes de la sesión', null=True, verbose_name='estado de paciente')),
                ('actividad', models.TextField(blank=True, null=True, verbose_name='actividades de la sesión')),
                ('comentarios', models.TextField(blank=True, null=True, verbose_name='comentarios')),
                ('motivo_consulta', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sesiones', to='tratamientos.MotivoConsulta')),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sesiones_paciente', to='pacientes.Paciente')),
            ],
            options={
                'verbose_name': 'sesión',
                'verbose_name_plural': 'sesiones',
            },
        ),
    ]
