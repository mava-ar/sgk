# Generated by Django 2.2.1 on 2019-05-23 03:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0008_auto_20180316_1758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='cobertura_medica',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='coberturas_medicas.Cobertura', verbose_name='cobertura'),
        ),
    ]