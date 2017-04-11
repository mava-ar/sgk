from django.core.urlresolvers import reverse, resolve

from test_plus.test import TestCase

from turnos.tests.factories import TurnoFactory


class TestUserURLs(TestCase):
    """Test URL patterns for turnos app."""

    def setUp(self):
        self.user = self.make_user()
        self.turno = TurnoFactory()

    def test_list(self):
        """turno_list should reverse to /turnos/."""
        self.assertEqual(reverse('turno_list'), '/turnos/')

    def test_list_resolve(self):
        """/turnos/ should resolve to turno_list."""
        self.assertEqual(resolve('/turnos/').view_name, 'turno_list')

    def test_new_object(self):
        self.assertEqual(reverse('turno_create'), '/turnos/nuevo/')

    def test_new_object_resolve(self):
        self.assertEqual(resolve('/turnos/nuevo/').view_name, 'turno_create')

    def test_edit_object(self):
        self.turno.save()  # get PK
        self.assertEqual(reverse('turno_update', args=(self.turno.pk, )),
                         '/turnos/editar/{}/'.format(self.turno.pk))

    def test_edit_object_resolve(self):
        self.turno.save()  # get PK
        self.assertEqual(resolve('/turnos/editar/{}/'.format(self.turno.pk)).view_name,
                         'turno_update')

    def test_delete_object(self):
        self.turno.save()  # get PK
        self.assertEqual(reverse('turno_delete', args=(self.turno.pk, )),
                         '/turnos/eliminar/{}/'.format(self.turno.pk))

    def test_report_object_resolve(self):
        self.turno.save()  # get PK
        self.assertEqual(resolve('/turnos/eliminar/{}/'.format(self.turno.pk)).view_name,
                         'turno_delete')

    def test_report_object(self):
        self.assertEqual(reverse('turno_report'), '/turnos/reporte/')

    def test_delete_object_resolve(self):
        self.assertEqual(resolve('/turnos/reporte/').view_name, 'turno_report')
