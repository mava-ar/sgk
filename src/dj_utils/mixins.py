from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin


class ShowInfoMixin(object):
    field_info = ()

    @property
    def show_info(self):
        """
        Retorna una diccionario con información. Si no se especifica field_info,
        se utilizará todos los campos.
        :return:
        """
        if not self.field_info:
            self.field_info = [f.name for f in self._meta.get_fields()]
        data = []
        for f in self.field_info:
            if hasattr(self, f):
                item = self._meta.get_field(f)
                data.append({'title': item.verbose_name.title(),
                             'field': item,
                             'typo': item.__class__.__name__,
                             'value': getattr(self, f)})
        return data


class FichaKinesicaMixin(object):
    """
    mixin utilizado en todos los métodos relativos a la ficha kinesica.
    Busca el paciente y lo incluye en el contexto.
    """
    def get_paciente(self):
        pk = self.kwargs.get('pk', None)
        if not pk:
            return HttpResponseRedirect(reverse('paciente_list'))
        from pacientes.models import Paciente
        self.paciente = Paciente.objects.get(pk=pk)
        return self.paciente

    def get_context_data(self, *args, **kwargs):
        context = super(FichaKinesicaMixin, self).get_context_data(*args, **kwargs)
        if not self.paciente:
            self.get_paciente()
        context["paciente"] = self.paciente
        from pacientes.models import EntradaHistoriaClinica
        context["entradas"] = EntradaHistoriaClinica.objects.select_subclasses().filter(
            paciente=self.paciente).order_by('-creado_el')
        return context

    def dispatch(self, request, *args, **kwargs):
        # siempre busco el paciente
        self.get_paciente()
        return super(FichaKinesicaMixin, self).dispatch(request, *args, **kwargs)


class ModelViewMixin(object):
    """
    Utilizar este mixin en las vistas que serán utilizadas con bootstrap modal.
    Exige definir un url_post_form para insertar en el template de manera de
    que el form cuente con un action válido.
    """
    template_name = "frontend/entrada_form.html"

    url_post_form = None

    def get_url_post_form(self):
        if self.url_post_form:
            return self.url_post_form
        raise NotImplemented("Debes definir este método en la subclase")

    def get_context_data(self, *args, **kwargs):
        ctx = super(ModelViewMixin, self).get_context_data(*args, **kwargs)
        ctx["url_post_form"] = self.get_url_post_form()
        return ctx


class FichaKinesicaModalView(FichaKinesicaMixin, ModelViewMixin):
    pass


class TableFilterListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    """
    Una vista que requiere autenticación, y espera que se defina la tabla y
    el filtrado de la misma
    """