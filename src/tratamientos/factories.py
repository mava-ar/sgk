# coding: utf-8
from datetime import timedelta
import factory

from django.utils import timezone

from core.factories import ProfesionalFactory
from tratamientos.models import MotivoConsulta, Objetivo, Planificacion, Sesion
from pacientes.factories import PacienteFactory


class MotivoConsultaFactory(factory.django.DjangoModelFactory):
    paciente = factory.SubFactory(PacienteFactory)
    motivo_consulta_paciente = factory.Faker('sentence', nb_words=6, locale='es')
    diagnostico_medico = factory.Faker('sentence', nb_words=4, locale='es')
    evaluacion_kinesica = factory.Faker('sentence', nb_words=10, locale='es')

    class Meta:
        model = MotivoConsulta


class ObjetivoFactory(factory.django.DjangoModelFactory):
    motivo_consulta = factory.SubFactory(MotivoConsultaFactory)
    descripcion = factory.Sequence(lambda n: 'objectivo %s' % n)

    class Meta:
        model = Objetivo


class PlanificacionFactory(factory.django.DjangoModelFactory):
    motivo_consulta = factory.SubFactory(MotivoConsultaFactory)
    fecha_ingreso = timezone.now()
    cantidad_sesiones = 10

    class Meta:
        model = Planificacion


class SesionFactory(factory.django.DjangoModelFactory):
    paciente = factory.SubFactory(PacienteFactory)
    profesional = factory.SubFactory(ProfesionalFactory)
    motivo_consulta = factory.SubFactory(MotivoConsultaFactory)
    fecha = timezone.now() - timedelta(days=1)
    comienzo_el = factory.SelfAttribute('fecha')
    fin_el = factory.LazyAttribute(
        lambda o: o.fecha + timedelta(minutes=o.duracion)
    )

    class Meta:
        model = Sesion
