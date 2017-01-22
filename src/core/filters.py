from crispy_forms.bootstrap import StrictButton
from django.db.models import Q

import django_filters
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout

from dj_utils.tables_filters import CrispyFilters
from .models import Persona


class PersonaListFilter(CrispyFilters):

    class PersonaListFormHelper(FormHelper):
        form_class = 'form-inline'
        form_method = 'get'
        layout = Layout(
            'nombre', 'genero', 'domicilio', 'profesion',
            StrictButton('<i class="material-icons">search</i>', type="submit", css_class='btn-fab btn-primary')
        )

    helper = PersonaListFormHelper

    nombre = django_filters.CharFilter(label='Nombre', method='nombre_paciente')
    domicilio = django_filters.CharFilter(label="Domicilio", lookup_expr='icontains')
    profesion = django_filters.CharFilter(label="Profesión", lookup_expr='icontains')

    def nombre_paciente(self, queryset, name, value):
        return queryset.filter(Q(nombre__icontains=value) | Q(apellido__icontains=value))

    class Meta:
        model = Persona
        fields = ['nombre', 'genero', 'domicilio', 'profesion']
