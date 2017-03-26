# coding=utf-8
from django.db.models import Q

import django_filters
from django_filters.widgets import RangeWidget
from crispy_forms.bootstrap import StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div

from dj_utils.tables_filters import CrispyFilters
from dj_utils.widgets import FechaWidget
from turnos.models import Turno


class TurnosReportFilter(CrispyFilters):

    class TurnosListFormHelper(FormHelper):
        form_class = 'form-inline'
        form_method = 'get'
        layout = Layout(
            Div('dia_start', 'dia_end', 'nombre'),
            Div('no_asistio', 'no_aviso', 'cobertura', 'profesional',
                StrictButton('<i class="material-icons">search</i>',
                             type="submit", css_class='btn btn-fab btn-primary'))
        )
    helper = TurnosListFormHelper

    def nombre_paciente(self, queryset, name, value):
        return queryset.select_related('paciente__persona').filter(
            Q(nombre_paciente__icontains=value) |
            Q(paciente__persona__nombre__icontains=value) |
            Q(paciente__persona__apellido__icontains=value))

    dia_start = django_filters.DateFilter(
        label='Desde el', name='dia', lookup_expr='dia__gte', widget=FechaWidget)
    dia_end = django_filters.DateFilter(
        label='Hasta el', name='dia', lookup_expr='dia__lte', widget=FechaWidget)
    nombre = django_filters.CharFilter(label='Nombre de paciente', method='nombre_paciente')
    no_asistio = django_filters.BooleanFilter(label='¿Faltó?', name='no_asistio')
    no_aviso = django_filters.BooleanFilter(label='¿Faltó y no avisó?', name='no_aviso')

    class Meta:
        model = Turno
        fields = ('dia_start', 'dia_end', 'nombre', 'no_asistio', 'no_aviso',
                  'cobertura', 'profesional')
