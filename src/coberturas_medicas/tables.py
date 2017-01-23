from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django_tables2 import URLColumn

from coberturas_medicas.models import Cobertura
from dj_utils.tables_filters import DefaultTable


class AccionesCoberturaColumn(URLColumn):
    def render(self, value, bound_column):
        url_edit = reverse('cobertura_update', args=(value, ))
        return mark_safe(u'<a href="{}" class="btn btn-fab btn-primary"><i class="material-icons">edit</i></a>'
                         u''.format(url_edit))


class CoberturaTable(DefaultTable):
    acciones = AccionesCoberturaColumn(verbose_name="Acciones", accessor='pk', orderable=False)

    class Meta(DefaultTable.Meta):
        model = Cobertura
        fields = ('nombre', 'codigo', 'telefono', 'direccion', 'email', 'acciones')
    