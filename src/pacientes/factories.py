# coding: utf-8
from datetime import datetime
import factory

from core.factories import PersonaFactory
from coberturas_medicas.factories import CoberturaFactory
from pacientes.models import Paciente


class PacienteFactory(factory.django.DjangoModelFactory):
    persona = factory.SubFactory(PersonaFactory)
    fecha_ingreso = factory.LazyFunction(datetime.now)
    cobertura_medica = factory.SubFactory(CoberturaFactory)

    class Meta:
        model = Paciente
