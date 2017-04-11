from datetime import timedelta

from django.core.urlresolvers import reverse
from django.test import RequestFactory
from django.utils.timezone import now

from test_plus.test import TestCase

from core.factories import ProfesionalFactory
from pacientes.factories import PacienteFactory
from turnos.tests.factories import TurnoFactory, TurnoPacienteNuevoFactory
from turnos.models import Turno


class BaseTurnoTestCase(TestCase):

    def setUp(self):
        self.user = self.make_user()
        self.factory = RequestFactory()
        self.profesional = ProfesionalFactory(usuario=self.user)
        self.client.login(
            username=self.user.username,
            password="password"
        )


class TestTurnoViews(BaseTurnoTestCase):

    def setUp(self):
        super(TestTurnoViews, self).setUp()

    def test_list(self):
        response = self.client.get(reverse('turno_list'))
        self.assertTemplateUsed(response, 'turnos/turno_list.html')

    def test_create(self):
        response = self.client.post(reverse('turno_create'), {
            'dia': '06/11/2016',
            'hora': '11:00',
            'duracion': 60,
            'nombre_paciente': 'Enrique Tolosa'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data="success-and-close"')
        self.assertNotContains(response, 'error')

        self.assertTrue(Turno.objects.filter(nombre_paciente='Enrique Tolosa').exists())

    def test_create_with_exists_patient(self):
        patient = PacienteFactory()
        response = self.client.post(reverse('turno_create'), {
            'dia': '06/11/2016',
            'hora': '11:00',
            'duracion': 60,
            'paciente_id': patient.id
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data="success-and-close"')
        self.assertNotContains(response, 'error')

    def test_edit(self):
        patient = PacienteFactory()
        turno = TurnoFactory(profesional=self.profesional, paciente=patient)
        turno.save()
        response = self.client.post(reverse('turno_update', args=(turno.id, )), {
            'dia': '06/11/2016',
            'hora': '11:00',
            'duracion': 60,
            'paciente_id': patient.id
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data="success-and-close"')
        self.assertNotContains(response, 'error')
        turno = Turno.objects.get(pk=turno.id)
        self.assertEqual(turno.dia.year, 2016)
        self.assertEqual(turno.dia.month, 11)
        self.assertEqual(turno.dia.day, 6)
        self.assertEqual(turno.hora.hour, 11)

    def test_Delete(self):
        turno = TurnoFactory(profesional=self.profesional)
        turno.save()
        response = self.client.post(
            reverse('turno_delete', args=(turno.id,)),
            data={}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data="success-and-close"')
        self.assertNotContains(response, 'error')
        self.assertFalse(Turno.objects.filter(pk=turno.id))

    def test_report(self):
        today = now()
        turno1 = TurnoFactory(profesional=self.profesional,
                              dia=today + timedelta(days=1))
        turno1.save()
        turno2 = TurnoPacienteNuevoFactory(
            profesional=self.profesional, dia=today + timedelta(days=3))
        turno2.save()
        turno3 = TurnoFactory(profesional=self.profesional,
                              dia=today + timedelta(days=4))
        turno3.save()

        response = self.client.get(reverse('turno_report'))
        self.assertEqual(response.context["filter"].qs.count(), 3)

        response = self.client.get("{}?nombre={}".format(
            reverse('turno_report'), turno2.nombre_paciente))
        self.assertEqual(response.context["filter"].qs.count(), 1)

        response = self.client.get("{}?dia_end={}".format(
            reverse('turno_report'),
            (today + timedelta(days=1)).strftime("%d/%m/%Y")))
        self.assertEqual(response.context["filter"].qs.count(), 1)

        response = self.client.get("{}?dia_start={}".format(
            reverse('turno_report'),
            (today + timedelta(days=2)).strftime("%d/%m/%Y")))
        self.assertEqual(response.context["filter"].qs.count(), 2)
