from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView
from django.views.generic import UpdateView

from coberturas_medicas.filters import CoberturaListFilter
from coberturas_medicas.models import Cobertura
from coberturas_medicas.tables import CoberturaTable

from dj_utils.mixins import TableFilterListView


class CoberturasListView(TableFilterListView):
    table_class = CoberturaTable
    filterset_class = CoberturaListFilter

    add_to_context = {
        "title": "Listado de coberturas",
        "create_link": reverse_lazy('cobertura_create')
    }


class CoberturaCreateView(LoginRequiredMixin, CreateView):
    template_name = 'frontend/base_edit_form.html'
    model = Cobertura
    fields = ('nombre', 'codigo', 'telefono', 'direccion', 'fax',
              'email', 'paga_por_sesion',)

    def get_context_data(self, **kwargs):
        ctx = super(CoberturaCreateView, self).get_context_data(**kwargs)
        ctx["model_name"] = self.model._meta.verbose_name
        ctx["return_link"] = reverse_lazy('cobertura_list')
        return ctx

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, "Cobertura médica agregada correctamente.")
        return reverse('cobertura_list')


class CoberturaUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'frontend/base_edit_form.html'
    model = Cobertura
    fields = ('nombre', 'codigo', 'telefono', 'direccion', 'fax',
              'email', 'paga_por_sesion',)

    def get_context_data(self, **kwargs):
        ctx = super(CoberturaUpdateView, self).get_context_data(**kwargs)
        ctx["model_name"] = self.model._meta.verbose_name
        ctx["return_link"] = reverse_lazy('cobertura_list')
        return ctx

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, "Entrada en la agenda modificada correctamente.")
        return reverse('cobertura_list')


cobertura_list = CoberturasListView.as_view()
cobertura_create = CoberturaCreateView.as_view()
cobertura_update = CoberturaUpdateView.as_view()
