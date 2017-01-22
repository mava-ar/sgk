from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django_tables2 import A, URLColumn

from dj_utils.tables_filters import DefaultTable, AvatarColumn
from .models import Paciente


class AccionesPacienteColumn(URLColumn):
    def render(self, value, bound_column):
        url_edit = reverse('paciente_update', args=(value, ))
        url_ficha = reverse('ficha_kinesica', args=(value, ))
        return mark_safe(u'<a href="{}" class="btn btn-fab btn-primary"><i class="material-icons">edit</i></a>'
                         u'<a href="{}" class="btn btn-fab btn-info"><i class="material-icons">assignment</i></a>'
                         u''.format(url_edit, url_ficha))


class PacienteTable(DefaultTable):
    avatar = AvatarColumn(verbose_name='', accessor=A('persona.avatar'), orderable=False)
    acciones = AccionesPacienteColumn(verbose_name="Acciones", accessor='pk', orderable=False)

    class Meta(DefaultTable.Meta):
        model = Paciente
        fields = ('avatar', 'persona.nombre',  'persona.apellido', 'fecha_ingreso', 'cobertura_medica',
                  'observaciones', 'acciones')
