# coding=utf-8
from django.conf import settings
from django.urls import reverse
from django.utils.safestring import mark_safe

from django_tables2 import A, URLColumn

from consultorio.models import Consultorio
from dj_utils.tables_filters import DefaultTable, AvatarColumn
from .models import Paciente


class AccionesPacienteColumn(URLColumn):
    def render(self, value, bound_column):
        consultorio = Consultorio.get_current()
        url_edit = reverse('paciente_update', args=(value, ))
        html = ('<a href="{}" class="btn btn-fab btn-primary" title="Editar paciente">'
                '<i class="material-icons">edit</i></a>').format(url_edit)
        if consultorio.plan > 1:
            url_ficha = reverse('ficha_kinesica', args=(value, ))
            url_tratamiento = reverse('tratamiento_list', args=(value, ))
            html += ('<a href="{}" class="btn btn-fab btn-info" title="Ver ficha kinésica">'
                     '<i class="material-icons">assignment</i></a>'
                     '<a href="{}" class="btn btn-fab btn-danger" title="Ver tratamientos" >'
                     '<i class="material-icons">event_available</i></a>'
                     ).format(url_ficha, url_tratamiento)
        return mark_safe(html)


class PacienteTable(DefaultTable):
    avatar = AvatarColumn(verbose_name='', accessor=A('persona.avatar'), orderable=False)
    acciones = AccionesPacienteColumn(verbose_name="Acciones", accessor='pk', orderable=False)

    class Meta(DefaultTable.Meta):
        model = Paciente
        fields = ('avatar', 'persona.nombre', 'persona.apellido', 'fecha_ingreso', 'modificado_el', 'cobertura_medica',
                  'observaciones', 'acciones')
        order_by = ['-modificado_el']
