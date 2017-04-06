from datetime import datetime, timedelta

from test_plus.test import TestCase

from core.factories import ProfesionalFactory
from turnos.tests.factories import TurnoFactory, TurnoPacienteNuevoFactory


class TestUser(TestCase):

    def setUp(self):
        self.user = self.make_user()
        self.profesional = ProfesionalFactory(usuario=self.user)

    def test__str__(self):
        turno_new = TurnoPacienteNuevoFactory(profesional=self.profesional)
        turno = TurnoFactory(profesional=self.profesional)

        self.assertEqual(turno_new.__str__(), "{} - {} {} ({})".format(
            turno_new.nombre_paciente, turno_new.dia, turno_new.hora, self.profesional
        ))
        self.assertEqual(turno.__str__(), "{} - {} {} ({})".format(
            turno.paciente, turno.dia, turno.hora, self.profesional
        ))

        turno_new.nombre_paciente = ''
        turno_new.save()
        self.assertEqual(turno_new.__str__(), "{} - {} {} ({})".format(
            "NN", turno_new.dia, turno_new.hora, self.profesional
        ))

    def test_api_properties_with_patients(self):
        turno = TurnoFactory(profesional=self.profesional)
        self.assertEqual(turno.datetime_start, datetime.combine(turno.dia, turno.hora))
        self.assertEqual(
            turno.datetime_end,
            datetime.combine(turno.dia, turno.hora) + timedelta(minutes=turno.duracion))
        self.assertEqual(turno.title, turno.paciente.__str__())
