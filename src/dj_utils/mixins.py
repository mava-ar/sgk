# coding=utf-8
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
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
        """
        if not self.field_info:
            self.field_info = [f.name for f in self._meta.get_fields()]
        data = []
        for f in self.field_info:
            if hasattr(self, f):
                item = self._meta.get_field(f)
                if hasattr(self, "get_{}_display".format(f)):
                    value = getattr(self, "get_{}_display".format(f))()
                else:
                    value = getattr(self, f)
                data.append({
                    'title': item.verbose_name.capitalize(),
                    'field': item,
                    'typo': item.__class__.__name__,
                    'value': value
                })
        return {
            'self': self,
            'information': data,
            'class_name': self.__class__._meta.verbose_name.capitalize(),
            'order': self.creado_el
        }


class FichaKinesicaMixin(object):
    """
    mixin utilizado en todos los métodos relativos a la ficha kinesica.
    Busca el paciente y lo incluye en el contexto.
    """
    def get_antecedente(self):
        """
        Retorna el antecedente, si este no existe, lo crea.
        """
        try:
            self.paciente.antecedente
        except ObjectDoesNotExist:
            from pacientes.models import Antecedente
            self.paciente.antecedente = Antecedente()
            self.paciente.antecedente.save()
        return self.paciente.antecedente

    def get_paciente(self):
        pk = self.kwargs.get('pk', None)
        if not pk:
            return HttpResponseRedirect(reverse('paciente_list'))
        from pacientes.models import Paciente
        self.paciente = Paciente.objects.get(pk=pk)
        self.get_antecedente()
        return self.paciente

    def get_context_data(self, *args, **kwargs):
        context = super(FichaKinesicaMixin, self).get_context_data(*args, **kwargs)
        if not self.paciente:
            self.get_paciente()
        context["paciente"] = self.paciente
        return context

    def dispatch(self, request, *args, **kwargs):
        # siempre busco el paciente
        self.get_paciente()
        return super(FichaKinesicaMixin, self).dispatch(request, *args, **kwargs)


class FichaKinesicaConHistoriaMixin(FichaKinesicaMixin):
    """
    Mixin utilizado para las vistas de ficha kinesica que requiera el historial médico.

    """
    HISTORIA_CLINICA_COMPLETE = False

    def get_context_data(self, *args, **kwargs):
        context = super(FichaKinesicaConHistoriaMixin, self).get_context_data(*args, **kwargs)
        return self.get_historia_clinica(context)

    def get_historia_clinica(self, context):
        entradas = [entradas.show_info for entradas in self.paciente.entradas_historiaclinica.select_subclasses().all()]
        if self.HISTORIA_CLINICA_COMPLETE:
            entradas.extend([sesion.show_info for sesion in self.paciente.sesiones_paciente.all()])
            entradas.extend([reg_bio.show_info for reg_bio in self.paciente.registros_biometricos.all()])
            entradas.extend([motivo.show_info for motivo in self.paciente.motivos_de_consulta.all()])
            for motivo in self.paciente.motivos_de_consulta.all():
                entradas.extend([plan.show_info for plan in motivo.planificaciones.all()])
                entradas.extend([objetivo.show_info for objetivo in motivo.objetivos.all()])
        context["entradas"] = sorted(entradas, key=lambda k: k['order'])
        return context


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
    template_name = 'frontend/base_list.html'

    add_to_context = {}

    def get_context_data(self, **kwargs):
        ctx = super(TableFilterListView, self).get_context_data(**kwargs)
        ctx.update(self.add_to_context)
        return ctx
