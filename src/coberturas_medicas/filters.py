import django_filters
from crispy_forms.bootstrap import StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout

from coberturas_medicas.models import Cobertura
from dj_utils.tables_filters import CrispyFilters


class CoberturaListFilter(CrispyFilters):
    class CoberturaListFormHelper(FormHelper):
        form_class = 'form-inline'
        form_method = 'get'
        layout = Layout(
            'nombre', 'codigo',
            StrictButton('<i class="material-icons">search</i>', type="submit", css_class='btn-fab btn-primary')
        )

    helper = CoberturaListFormHelper

    nombre = django_filters.CharFilter(label='Nombre', lookup_expr='icontains')
    codigo = django_filters.CharFilter(label="Código", lookup_expr='icontains')

    class Meta:
        model = Cobertura
        fields = ('nombre', 'codigo', )
