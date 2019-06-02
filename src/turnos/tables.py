# coding=utf-8
from django.utils.safestring import mark_safe
from django.urls import reverse_lazy

from django_tables2 import A, URLColumn, BooleanColumn, Column

from dj_utils.tables_filters import DefaultTable
from .models import Turno


class TurnosReporteTable(DefaultTable):
    no_asistio = BooleanColumn(verbose_name='¿Faltó?', accessor='no_asistio')
    no_aviso = BooleanColumn(verbose_name='¿Faltó y no avisó?', accessor='no_aviso')
    paciente = Column(verbose_name='Nombre el paciente', empty_values=())

    class Meta(DefaultTable.Meta):
        model = Turno
        fields = ('dia', 'hora', 'paciente', 'motivo', 'duracion', 'no_asistio',
                  'no_aviso', 'profesional', 'cobertura')

    def render_paciente(self, record):
        if record.paciente_id:
            return mark_safe('<a href="{}">{}</a>'.format(
                reverse_lazy('paciente_update', args=(record.paciente.pk, )),
                record.paciente))
        return "{}".format(record.nombre_paciente)
