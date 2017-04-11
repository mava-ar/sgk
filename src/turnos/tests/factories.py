# coding:utf-8
from datetime import datetime, timedelta
import factory

from core.factories import ProfesionalFactory
from pacientes.factories import PacienteFactory
from turnos.models import Turno


class TurnoPacienteNuevoFactory(factory.Factory):
    dia = factory.Faker('date_time_between', start_date="now", end_date="+10d")
    hora = factory.LazyAttribute(lambda obj: obj.dia.time())
    profesional = factory.SubFactory(ProfesionalFactory)
    # optional
    nombre_paciente = factory.Faker('name', locale='es')
    motivo = factory.Faker('sentence', nb_words=4)

    class Meta:
        model = Turno


class TurnoFactory(factory.Factory):
    dia = factory.Faker('date_time_between', start_date="now", end_date="+10d")
    hora = factory.LazyAttribute(lambda obj: obj.dia.time())
    profesional = factory.SubFactory(ProfesionalFactory)
    # optional
    paciente = factory.SubFactory(PacienteFactory)

    class Meta:
        model = Turno
