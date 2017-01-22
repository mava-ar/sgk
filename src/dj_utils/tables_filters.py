import django_filters
from django.utils.html import format_html
from django_tables2 import Column
from django_tables2 import Table


class CrispyFilters(django_filters.FilterSet):
    """
    Inserte el helper de crispy en el form del filtro si se define `helper`
    """
    helper = None

    @property
    def form(self):
        self._form = super(CrispyFilters, self).form
        if self.helper is not None:
            self._form.helper = self.helper()
            self._form.helper.form_method = 'get'
            self._form.helper.form_action = '.'
        return self._form


class DefaultTable(Table):
    """
    Una tabla con las definiciones por default para el sistema.
    Heredar de esta clase todas las tablas.
    """
    class Meta:
        def __init__(self):
            super().__init__()
        template = 'django_tables2/bootstrap.html'
        attrs = {'class': 'table table-condensed table-striped'}


class AvatarColumn(Column):
    def render(self, value):
        return format_html('<img class="img-circle" src="{}" />', value)
