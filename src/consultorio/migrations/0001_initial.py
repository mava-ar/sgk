# Generated by Django 2.2.1 on 2019-05-23 03:36

from django.db import migrations, models
import django.db.models.deletion
import django_tenants.postgresql_backend.base


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Consultorio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schema_name', models.CharField(db_index=True, max_length=63, unique=True, validators=[django_tenants.postgresql_backend.base._check_schema_name])),
                ('creado_el', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('modificado_el', models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')),
                ('nombre', models.CharField(max_length=100)),
                ('pagado_hasta', models.DateField(blank=True, null=True)),
                ('on_trial', models.BooleanField(default=True)),
                ('plan', models.IntegerField(choices=[(1, 'Básico'), (2, 'Estándar'), (3, 'Premium')], default=1)),
            ],
            options={
                'verbose_name': 'consultorio',
                'verbose_name_plural': 'consultorios',
            },
        ),
        migrations.CreateModel(
            name='Dominio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(db_index=True, max_length=253, unique=True)),
                ('is_primary', models.BooleanField(db_index=True, default=True)),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='domains', to='consultorio.Consultorio')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
