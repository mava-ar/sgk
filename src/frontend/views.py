from datetime import datetime, timedelta, time

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db.transaction import atomic
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.contrib import messages
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DetailView

from enhanced_cbv.views.edit import InlineFormSetsView, EnhancedInlineFormSet

from core.forms import PersonaForm, ContactoForm
from core.models import Persona, Profesion, Profesional
from pacientes.forms import PacienteForm, AntecedenteForm
from pacientes.models import Paciente, Antecedente
from tratamientos.forms import ObjetivoInlineForm, MotivoConsultaForm, ObjetivoInlineFormset
from tratamientos.models import MotivoConsulta, Objetivo
from turnos.forms import TurnoForm
from turnos.models import Turno


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'frontend/index.html'


class AboutView(LoginRequiredMixin, TemplateView):
    template_name = "frontend/about.html"


class TurnosListView(LoginRequiredMixin, ListView):

    def get_queryset(self):

        dt = datetime.combine(timezone.now(), time.min)
        dt_limit = dt + timedelta(days=14)
        return Turno.objects.filter(dia__gte=dt).order_by('dia', 'hora')


class TurnoCreateView(LoginRequiredMixin, CreateView):
    model = Turno
    form_class = TurnoForm

    def get_initial(self):
        try:
            profesional = Profesional.objects.get(usuario=self.request.user)
            self.initial.update({'profesional': profesional})
        except ObjectDoesNotExist:
            pass
        return super(TurnoCreateView, self).get_initial()

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS,
                             "Turno creado correctamente.")
        return reverse('turno_list')


class TurnoEditView(LoginRequiredMixin, UpdateView):
    model = Turno
    form_class = TurnoForm

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS,
                             "Turno actualizado correctamente.")
        return reverse('turno_list')


class PacienteListView(LoginRequiredMixin, ListView):

    def get_queryset(self):
        return Paciente.objects.all()


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
                u"Paciente creado correctamente.")
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
                u"Paciente editado correctamente.")
        return reverse('paciente_list')


class PersonaListView(LoginRequiredMixin, ListView):
    template_name = "core/persona_list.html"

    def get_queryset(self):
        return Persona.objects.all()


class PersonaCreateView(LoginRequiredMixin, CreateView):
    model = Persona
    fields = ('nombre', 'apellido', 'fecha_nacimiento', 'genero', 'estado_civil',
              'dni', 'domicilio', 'imagen_perfil', 'observaciones', )

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, "Entrada en la agenda añadida correctamente.")
        return reverse('persona_list')


class FichaKinesicaMixin(object):
    """
    mixin utilizado en todos los métodos relativos a la ficha kinesica.
    Busca el paciente y lo incluye en el contexto.
    """
    def get_paciente(self):
        pk = self.kwargs.get('pk', None)
        if not pk:
            return HttpResponseRedirect(reverse('paciente_list'))
        self.paciente = Paciente.objects.get(pk=pk)
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


class FichaKinesicaIndex(LoginRequiredMixin, FichaKinesicaMixin, TemplateView):
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

    # def get_context_data(self, *args, **kwargs):
    #     context = super(FichaKinesicaIndex, self).get_context_data(*args, **kwargs)
    #     context["paciente"] = self.paciente
    #     return context


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


class MotivoConsultaIndex(LoginRequiredMixin, FichaKinesicaMixin, ListView):
    template_name = "frontend/motivo_list.html"
    model = MotivoConsulta

    def get_queryset(self):
        return self.get_paciente().motivos_de_consulta.all().order_by('-creado_el')


class MotivosConsultaAddView(LoginRequiredMixin, FichaKinesicaMixin, CreateView):
    model = MotivoConsulta
    template_name = "frontend/motivo_form.html"
    form_class = MotivoConsultaForm

    def get_context_data(self, *args, **kwargs):
        context = super(MotivosConsultaAddView, self).get_context_data(*args, **kwargs)
        if self.request.POST:
            context['objetivo_formset'] = ObjetivoInlineFormset(self.request.POST)
        else:
            context['objetivo_formset'] = ObjetivoInlineFormset()
        return context

    def post(self, request, *args, **kwargs):
        import ipdb;ipdb.set_trace()
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        objectivo_formset = ObjetivoInlineFormset(self.request.POST)
        if form.is_valid() and objectivo_formset.is_valid():
            return self.form_valid(form, objectivo_formset)
        else:
            return self.form_invalid(form, objectivo_formset)

    @atomic
    def form_valid(self, form, objetivo_formset):
        import ipdb;ipdb.set_trace()
        motivo = form.save(commit=False)
        motivo.paciente = self.paciente
        motivo.save()
        objetivo_formset.instance = motivo
        objetivo_formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, objetivo_formset):
        return super(MotivosConsultaAddView, self).form_invalid(form)

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS,
            u"Motivo de consulta añadido correctamente.")
        return reverse('motivo_consulta', kwargs={'pk': self.paciente.pk})




index = IndexView.as_view()
about = AboutView.as_view()
persona_list = PersonaListView.as_view()
persona_create = PersonaCreateView.as_view()
turno_list = TurnosListView.as_view()
turno_create = TurnoCreateView.as_view()
turno_update = TurnoEditView.as_view()
paciente_list = PacienteListView.as_view()
paciente_create = PacienteCreateView.as_view()
paciente_update = PacienteEditView.as_view()
ficha_kinesica = FichaKinesicaIndex.as_view()
ficha_kinesica_update = FichaKinesicaEditView.as_view()
motivo_consulta = MotivoConsultaIndex.as_view()
motivo_consulta_create = MotivosConsultaAddView.as_view()