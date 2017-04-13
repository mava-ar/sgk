from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.transaction import atomic
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone
from django.views.generic import TemplateView, CreateView, UpdateView, DetailView
from enhanced_cbv.views.edit import InlineFormSetsView

from core.filters import PersonaListFilter
from core.forms import PersonaForm, ContactoForm
from core.models import Persona
from core.tables import PersonaTable
from dj_utils.mixins import (
    FichaKinesicaMixin, FichaKinesicaConHistoriaMixin, FichaKinesicaModalView,
    TableFilterListView)
from pacientes.filters import PacienteListFilter
from pacientes.forms import PacienteForm, AntecedenteForm
from pacientes.models import Paciente, Antecedente, ComentariosHistoriaClinica, ImagenesHistoriaClinica, \
    EntradaHistoriaClinica
from pacientes.tables import PacienteTable


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'frontend/index.html'

    def get(self, request, **kwargs):
        """
        Hasta construir el dashboard, redireccionamos a turnos
        """
        return HttpResponseRedirect(reverse('turno_list'))


class PacienteListView(TableFilterListView):
    table_class = PacienteTable
    filterset_class = PacienteListFilter
    template_name = 'pacientes/paciente_list.html'


class PacienteCreateView(LoginRequiredMixin, CreateView):
    model = Paciente
    form_class = PacienteForm

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        persona_form = PersonaForm()
        contacto_form = ContactoForm()
        return self.render_to_response(self.get_context_data(
            form=form, persona_form=persona_form, contacto_form=contacto_form))

    def get_initial(self):
        hoy = timezone.now()
        self.initial.update({'fecha_ingreso': hoy})
        return super(PacienteCreateView, self).get_initial()

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        persona_form = PersonaForm(self.request.POST, self.request.FILES)
        contacto_form = ContactoForm(self.request.POST)
        if form.is_valid() and persona_form.is_valid() and contacto_form.is_valid():
            return self.form_valid(form, persona_form, contacto_form)
        else:
            return self.form_invalid(form, persona_form, contacto_form)

    @atomic
    def form_valid(self, form, persona_form, contacto_form):
        persona = persona_form.save(commit=False)
        contacto = contacto_form.save(commit=False)
        self.object = form.save(commit=False)
        contacto.nombre = persona.nombre
        contacto.apellido = persona.apellido
        contacto.save()
        persona.contacto = contacto
        persona.save()
        self.object.persona = persona
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, persona_form, contacto_form):

        return self.render_to_response(
            self.get_context_data(form=form, persona_form=persona_form, contacto_form=contacto_form))

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS,
                             "Paciente creado correctamente.")
        return reverse('paciente_list')


class PacienteEditView(LoginRequiredMixin, UpdateView):
    model = Paciente
    form_class = PacienteForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        persona_form = PersonaForm(instance=self.object.persona)
        contacto_form = ContactoForm(instance=self.object.persona.info_contacto if self.object.persona.info_contacto else None)
        return self.render_to_response(
            self.get_context_data(form=form,
                                  persona_form=persona_form,
                                  contacto_form=contacto_form))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        persona_form = PersonaForm(self.request.POST, self.request.FILES, instance=self.object.persona)
        contacto_form = ContactoForm(self.request.POST, instance=self.object.persona.info_contacto)
        if form.is_valid() and persona_form.is_valid()\
                and contacto_form.is_valid():
            return self.form_valid(form, persona_form, contacto_form)
        else:
            return self.form_invalid(form, persona_form, contacto_form)

    @atomic
    def form_valid(self, form, persona_form, contacto_form):
        persona = persona_form.save(commit=False)
        contacto = contacto_form.save(commit=False)
        self.object = form.save(commit=False)
        contacto.nombre = persona.nombre
        contacto.apellido = persona.apellido
        contacto.save()
        persona.info_contacto = contacto
        persona.save()
        self.object.persona = persona
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, persona_form, contacto_form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form,
                                  persona_form=persona_form,
                                  contacto_form=contacto_form))

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS,
                             "Paciente editado correctamente.")
        return reverse('paciente_list')


class PersonaListView(TableFilterListView):
    template_name = "core/persona_list.html"
    table_class = PersonaTable
    filterset_class = PersonaListFilter


class PersonaCreateView(LoginRequiredMixin, CreateView):
    model = Persona
    fields = ('nombre', 'apellido', 'fecha_nacimiento', 'genero', 'estado_civil',
              'dni', 'domicilio', 'imagen_perfil', 'observaciones', )

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, "Entrada en la agenda añadida correctamente.")
        return reverse('persona_list')


class PersonaUpdateView(LoginRequiredMixin, UpdateView):
    model = Persona
    form_class = PersonaForm

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, "Entrada en la agenda modificada correctamente.")
        return reverse('persona_list')


class FichaKinesicaIndex(LoginRequiredMixin, FichaKinesicaConHistoriaMixin, TemplateView):
    template_name = "frontend/ficha_kinesica.html"

    def get_object(self, queryset=None):
        try:
            return self.paciente.antecedente
        except ObjectDoesNotExist:
            self.paciente.antecedente = Antecedente()
            self.paciente.antecedente.save()
            return self.paciente.antecedente

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(FichaKinesicaIndex, self).get(request, *args, **kwargs)


class FichaKinesicaEditView(LoginRequiredMixin, FichaKinesicaMixin, InlineFormSetsView):
    """
    El ID dado será del paciente, de debe buscar el antecedente
    """
    template_name = "frontend/antecedente_form.html"
    model = Antecedente
    form_class = AntecedenteForm

    # class ObjetivoInline(EnhancedInlineFormSet):
    #     formset_class = ObjetivoInlineForm
    #     model = Objetivo
    #     extra = 0
    #     can_delete = True
    #
    # formsets = [ObjetivoInline, ]

    # def get_factory_kwargs(self):
    #     return {
    #         'parent_model': MotivoConsulta
    #     }

    def get_object(self, queryset=None):
        try:
            return self.paciente.antecedente
        except ObjectDoesNotExist:
            self.paciente.antecedente = Antecedente()
            self.paciente.antecedente.save()
            return self.paciente.antecedente


    # def get_motivo_instance(self):
    #     if self.kwargs.get('motivo_pk', None):
    #         return self.object.paciente.motivos_de_consulta.get(
    #             pk=self.kwargs.get('motivo_pk', None))
    #     else:
    #         return self.object.paciente.motivos_de_consulta.latest('fecha_ingreso')
    #
    # def post(self, request, *args, **kwargs):
    #     return super(FichaKinesicaEditView, self).post(request, *args, **kwargs)

    # def form_valid(self, form):
    #     motivo_form = self.get_motivo_form()
    #     motivo_form.save()
    #     return super(FichaKinesicaEditView, self).form_valid(form)

    # def get_formsets_kwargs(self, enhanced_formset):
    #     kwargs = super(FichaKinesicaEditView, self).get_formsets_kwargs(enhanced_formset)
    #     kwargs.update({
    #         'instance': self.get_motivo_instance()
    #     })
    #     return kwargs
    #
    # def get_motivo_form(self):
    #     if self.request.method == "POST":
    #         return MotivoConsultaForm(self.request.POST,
    #                                   instance=self.get_motivo_instance())
    #     else:
    #         return MotivoConsultaForm(instance=self.get_motivo_instance())

    def get_context_data(self, *args, **kwargs):
        context = super(FichaKinesicaEditView, self).get_context_data(*args, **kwargs)
        #context["form"] = self.get_form(self.get_form_class())
        # context["paciente"] = self.object.paciente
        # context["motivo_form"] = self.get_motivo_form()
        context["motivos"] = self.object.paciente.motivos_de_consulta.all()
        return context

    def get_success_url(self, *args, **kwargs):
        messages.add_message(self.request, messages.SUCCESS,
            u"Ficha editada correctamente.")
        return reverse('ficha_kinesica', kwargs={'pk': self.paciente.pk})
        # if self.kwargs.get('motivo_pk', None):
        #     motivo_pk = self.kwargs.get('motivo_pk', None)
        #     return reverse('ficha_kinesica', kwargs={'pk': pk, 'motivo_pk': motivo_pk})
        # else:
        #     return reverse('ficha_kinesica', kwargs={'pk': pk})


class AbstractEntradaHistoriaClinicaCreate(LoginRequiredMixin, FichaKinesicaModalView, CreateView):

    def form_valid(self, form):
        entrada = form.save(commit=False)
        entrada.profesional = self.request.user.profesional
        entrada.paciente = self.paciente
        entrada.save()
        return HttpResponse(render_to_string('frontend/entrada_form_success.html',
                                             {'object': self.paciente, 'state': 'new'}))


class ComentarioHCViewCreate(AbstractEntradaHistoriaClinicaCreate):
    model = ComentariosHistoriaClinica
    fields = ('comentarios', )

    def get_url_post_form(self):
        return reverse_lazy('comentario_hc_create', kwargs={'pk': self.paciente.pk})


class ImagenesHCViewCreate(AbstractEntradaHistoriaClinicaCreate):
    model = ImagenesHistoriaClinica
    fields = ('imagen', 'comentarios', )

    def get_url_post_form(self):
        return reverse_lazy('imagen_hc_create', kwargs={'pk': self.paciente.pk})


class AbstractEntradaHistoriaClinicaUpdate(LoginRequiredMixin, FichaKinesicaModalView, UpdateView):

    def form_valid(self, form):
        form.save()
        return HttpResponse(render_to_string('frontend/entrada_form_success.html',
                                             {'object': self.paciente, 'state': 'update'}))


class ComentarioHCViewUpdate(AbstractEntradaHistoriaClinicaUpdate):
    model = ComentariosHistoriaClinica
    fields = ('comentarios', )
    pk_url_kwarg = 'pk_comentario'

    def get_url_post_form(self):
        return reverse_lazy('comentario_hc_update', kwargs={'pk': self.paciente.pk, 'pk_comentario': self.object.pk })


class ImagenesHCViewUpdate(AbstractEntradaHistoriaClinicaUpdate):
    model = ImagenesHistoriaClinica
    fields = ('imagen', 'comentarios', )
    pk_url_kwarg = 'pk_imagen'

    def get_url_post_form(self):
        return reverse_lazy('imagen_hc_update', kwargs={'pk': self.paciente.pk, 'pk_imagen': self.object.pk})


class HistoriaClinicaListView(LoginRequiredMixin, FichaKinesicaConHistoriaMixin, DetailView):
    model = Paciente

    def get(self, request, *args, **kwargs):
        self.object = self.paciente
        self.template_name = "includes/historia_clinica_entradas_list.html"
        context = self.get_context_data()
        return self.render_to_response(context)


index = IndexView.as_view()
persona_list = PersonaListView.as_view()
persona_create = PersonaCreateView.as_view()
persona_update = PersonaUpdateView.as_view()
paciente_list = PacienteListView.as_view()
paciente_create = PacienteCreateView.as_view()
paciente_update = PacienteEditView.as_view()
ficha_kinesica = FichaKinesicaIndex.as_view()
ficha_kinesica_update = FichaKinesicaEditView.as_view()
comentario_hc_create = ComentarioHCViewCreate.as_view()
comentario_hc_update = ComentarioHCViewUpdate.as_view()
imagen_hc_create = ImagenesHCViewCreate.as_view()
imagen_hc_update = ImagenesHCViewUpdate.as_view()
historia_clinica_list = HistoriaClinicaListView.as_view()
