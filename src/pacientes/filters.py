from crispy_forms.bootstrap import StrictButton
from django.db.models import Q

import django_filters
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout

from dj_utils.tables_filters import CrispyFilters
from .models import Paciente


class PacienteListFilter(CrispyFilters):

    class PacienteListFormHelper(FormHelper):
        form_class = 'form-inline'
        form_method = 'get'
        layout = Layout(
            'nombre', 'cobertura_medica',
            StrictButton('<i class="material-icons">search</i>', type="submit", css_class='btn btn-fab btn-primary')
        )

    helper = PacienteListFormHelper

    nombre = django_filters.CharFilter(label='Nombre', method='nombre_paciente')

    def nombre_paciente(self, queryset, name, value):
        return queryset.select_related('persona').filter(Q(persona__nombre__icontains=value) |
                                                         Q(persona__apellido__icontains=value))

    class Meta:
        model = Paciente
        fields = ['nombre', 'cobertura_medica']
