from django.urls import reverse
from django.utils.safestring import mark_safe
from django_tables2 import A, URLColumn
from django_tables2 import Column

from dj_utils.tables_filters import DefaultTable, AvatarColumn
from .models import Persona


class AccionesPersonaColumn(URLColumn):
    def render(self, value, bound_column):
        url_edit = reverse('persona_update', args=(value, ))
        return mark_safe(u'<a href="{}" class="btn btn-fab btn-primary"><i class="material-icons">edit</i></a>'
                         u''.format(url_edit))


class PersonaTable(DefaultTable):
    avatar = AvatarColumn(verbose_name='', accessor=A('avatar'), orderable=False)
    contacto = Column(empty_values=[])
    acciones = AccionesPersonaColumn(verbose_name="Acciones", accessor='pk', orderable=False)

    def render_contacto(self, record):
        if record.info_contacto:
            return ' | '.join([x for x in record.info_contacto.get_basic_info()])
        return "-"

    class Meta(DefaultTable.Meta):
        model = Persona
        fields = ('avatar', 'nombre', 'apellido', 'fecha_nacimiento', 'edad', 'genero',
                  'estado_civil', 'DNI', 'domicilio', 'profesion', 'contacto', 'observaciones', 'acciones')
