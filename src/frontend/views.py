from datetime import datetime, timedelta, time

import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db.transaction import atomic
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone
from django.contrib import messages
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView

from enhanced_cbv.views.edit import InlineFormSetsView, EnhancedInlineFormSet

from core.forms import PersonaForm, ContactoForm
from core.models import Persona, Profesion, Profesional
from pacientes.forms import PacienteForm, AntecedenteForm
from pacientes.models import Paciente, Antecedente
from tratamientos.forms import (ObjetivoForm, MotivoConsultaForm, ObjetivoInlineFormset,
                                ObjetivoCumplidoUpdateForm, PlanificacionCreateForm, NuevaSesionForm)
from tratamientos.models import MotivoConsulta, Objetivo, Planificacion, Sesion
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
        return Turno.objects.exclude(sesion__fin_el__isnull=False).filter(dia__gte=dt).order_by('dia', 'hora')


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


class TratamientoListView(LoginRequiredMixin, FichaKinesicaMixin, ListView):
    template_name = "frontend/tratamiento_list.html"
    model = MotivoConsulta

    def get_queryset(self):
        return self.get_paciente().motivos_de_consulta.all().order_by('-creado_el')


class TratamientoAddView(LoginRequiredMixin, FichaKinesicaMixin, CreateView):
    model = MotivoConsulta
    template_name = "frontend/tratamiento_form.html"
    form_class = MotivoConsultaForm

    def get(self, request, *args, **kwargs):
        # estados = [Planificacion.PLANIFICADO, Planificacion.EN_CURSO, ]
        if self.paciente.motivos_de_consulta.filter(planificaciones__estado__in=[1,2]):
            messages.add_message(
                self.request, messages.ERROR, "Existe un tratamiento en curso en este momento. "
                                              "Finalicelo antes de iniciar otro.")
            return HttpResponseRedirect(
                reverse('tratamiento_list', kwargs={'pk': self.paciente.pk}))
        return super(TratamientoAddView, self).get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(TratamientoAddView, self).get_context_data(*args, **kwargs)
        if self.request.POST:
            context['objetivo_formset'] = ObjetivoInlineFormset(self.request.POST)
            context["tratamiento_form"] = PlanificacionCreateForm(self.request.POST)
        else:
            context["tratamiento_form"] = PlanificacionCreateForm()
            context['objetivo_formset'] = ObjetivoInlineFormset()
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        objectivo_formset = ObjetivoInlineFormset(self.request.POST)
        tratamiento_form = PlanificacionCreateForm(self.request.POST)
        if form.is_valid() and objectivo_formset.is_valid() and tratamiento_form.is_valid():
            return self.form_valid(form, objectivo_formset, tratamiento_form)
        else:
            return self.form_invalid(form, objectivo_formset, tratamiento_form)

    @atomic
    def form_valid(self, form, objetivo_formset, tratamiento_form):
        motivo = form.save(commit=False)
        motivo.paciente = self.paciente
        motivo.save()
        objetivo_formset.instance = motivo
        objetivo_formset.save()
        planificacion = tratamiento_form.save(commit=False)
        planificacion.motivo_consulta = motivo
        planificacion.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, objetivo_formset, tratamiento_form):
        return super(TratamientoAddView, self).form_invalid(form)

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS,
                             "Tratamiento añadido correctamente.")
        return reverse('tratamiento_list', kwargs={'pk': self.paciente.pk})


class TratamientoEditView(LoginRequiredMixin, FichaKinesicaMixin, UpdateView):
    model = MotivoConsulta
    template_name = "frontend/tratamiento_form.html"
    form_class = MotivoConsultaForm

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk_motivo', None)
        self.object = MotivoConsulta.objects.get(paciente_id=self.paciente.pk, id=pk)
        return self.object

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        tratamiento_form = PlanificacionCreateForm(instance=self.object.planificaciones.last())
        objetivo_form = ObjetivoInlineFormset(instance=self.object)
        return self.render_to_response(self.get_context_data(
            form=form, objetivo_formset=objetivo_form, tratamiento_form=tratamiento_form))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        objectivo_formset = ObjetivoInlineFormset(self.request.POST, instance=self.object)
        tratamiento_form = PlanificacionCreateForm(self.request.POST, instance=self.object.planificaciones.last())
        if form.is_valid() and objectivo_formset.is_valid() and tratamiento_form.is_valid():
            return self.form_valid(form, objectivo_formset, tratamiento_form)
        else:
            return self.form_invalid(form, objectivo_formset, tratamiento_form)

    @atomic
    def form_valid(self, form, objetivo_formset, tratamiento_form):
        motivo = form.save()
        # motivo.paciente = self.paciente
        # motivo.save()
        # objetivo_formset.instance = motivo
        objetivo_formset.save()
        planificacion = tratamiento_form.save()
        # planificacion.motivo_consulta = motivo
        # planificacion.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, objetivo_formset, tratamiento_form):
        return super(TratamientoEditView, self).form_invalid(form)

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS,
                             "Tratamiento actualizado correctamente.")
        return reverse('tratamiento_list', kwargs={'pk': self.paciente.pk})

# class MotivosConsultaEditView(LoginRequiredMixin, FichaKinesicaMixin, UpdateView):
#     model = MotivoConsulta
#     template_name = "frontend/motivo_form.html"
#     form_class = MotivoConsultaForm
#
#     def get_object(self, queryset=None):
#         pk = self.kwargs.get('pk_motivo', None)
#         return MotivoConsulta.objects.get(paciente_id=self.paciente.pk, id=pk)
#
#     def get_success_url(self):
#         messages.add_message(self.request, messages.SUCCESS,
#             u"Motivo de consulta modificado correctamente.")
#         return reverse('planificacion_create', kwargs={'pk': self.paciente.pk,
#                                                        'pk_objetivo': self.object.pk})
        # return reverse('motivo_consulta', kwargs={'pk': self.paciente.pk})

#
class ObjetivoEditView(LoginRequiredMixin, FichaKinesicaMixin, UpdateView):
    model = Objetivo
    template_name = "frontend/objetivo_form.html"
    form_class = ObjetivoForm

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk_objetivo', None)
        self.object = Objetivo.objects.get(pk=pk)
        return self.object

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS,
                             "Objetivo modificado correctamente.")
        return reverse('tratamiento_list', kwargs={'pk': self.paciente.pk})


# class ObjetivoToggleCheckView(LoginRequiredMixin, UpdateView):
#     model = Objetivo
#     form_class = ObjetivoCumplidoUpdateForm
#
#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         form = ObjetivoCumplidoUpdateForm(request.POST, instance=self.object)
#         if form.is_valid():
#             self.object = form.save(commit=False)
#             self.object.fecha_cumplido = None if self.object.fecha_cumplido else timezone.now()
#             self.object.save()
#         return HttpResponse(json.dumps(
#             {
#                 'fecha_cumplido': self.object.fecha_cumplido
#             }), content_type='application/json')


# class PlanificacionCreateView(LoginRequiredMixin, FichaKinesicaMixin, CreateView):
#     model = Planificacion
#     form_class = PlanificacionCreateForm
#     template_name = "frontend/planificacion_form.html"
#
#     def get_motivo(self):
#         pk = self.kwargs.get('pk_motivo', None)
#         return MotivoConsulta.objects.get(paciente_id=self.paciente.pk, id=pk)
#
#     def form_valid(self, form):
#         import ipdb;ipdb.set_trace()
#         planificacion = form.save(commit=False)
#         planificacion.motivo_consulta = self.get_motivo()
#         planificacion.save()
#         return HttpResponseRedirect(self.get_success_url())
#
#     def get_success_url(self):
#         messages.add_message(self.request, messages.SUCCESS,
#                              "La planificación del tratamiento fue establecido con éxito.")
#         return reverse('motivo_consulta', kwargs={'pk': self.paciente.pk})
#
#     def get_context_data(self, *args, **kwargs):
#         context = super(PlanificacionCreateView, self).get_context_data(*args, **kwargs)
#         context["motivo"] = self.get_motivo()
#         return context


class SesionCreateView(LoginRequiredMixin, FichaKinesicaMixin, UpdateView):
    model = Sesion
    form_class = NuevaSesionForm
    template_name = "frontend/sesion_form.html"

    # def dispatch(self, request, *args, **kwargs):
    #     super(SesionCreateView, self).dispatch(request, *args, **kwargs)
    #     # marcar el turno como asistido.
    #
    def check_turno(self):
        try:
            self.object.turno_dado
        except Turno.DoesNotExist:
            turno_pk = self.request.GET.get('turno', None)
            if turno_pk:
                turno = Turno.objects.get(pk=turno_pk)
                turno.asistio = True
                turno.sesion = self.object
                turno.save()

    def get_object(self, queryset=None):
        try:
            self.object = Sesion.objects.get(paciente=self.paciente, motivo_consulta=self.get_motivo(), fin_el__isnull=True)
        except ObjectDoesNotExist:
            # la sesión es nueva
            self.object = Sesion(paciente=self.paciente, motivo_consulta=self.motivo, fecha=timezone.now())
            self.object.save()
        self.check_turno()
        return self.object

    def save_and_post_actions(self, sesion):
        plan = sesion.motivo_consulta.planificacion_actual
        if plan.estado == Planificacion.PLANIFICADO:
            plan.estado = Planificacion.EN_CURSO
            plan.save()
        sesion.save()

    def get_motivo(self):
        pk = self.kwargs.get('pk_motivo', None)
        self.motivo = MotivoConsulta.objects.get(paciente_id=self.paciente.pk, id=pk)
        return self.motivo

    def form_valid(self, form):
        sesion = form.save(commit=False)
        if not sesion.fecha:
            sesion.fecha = timezone.now()
        self.save_and_post_actions(sesion)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS,
                             "La sesión fue guardada correctamente.")
        return reverse('sesion_create',
                       kwargs={'pk': self.paciente.pk, 'pk_motivo': self.paciente.tratamiento_activo().pk })

    def get_context_data(self, *args, **kwargs):
        context = super(SesionCreateView, self).get_context_data(*args, **kwargs)
        context["motivo"] = self.get_motivo()
        return context


class SesionSaveAndCloseView(SesionCreateView):
    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS,
                             "La sesión fue guardada y finalizada correctamente.")
        return reverse('turno_list')

    def save_and_post_actions(self, sesion):
        sesion.fin_el = timezone.now()
        super(SesionSaveAndCloseView, self).save_and_post_actions(sesion)


class SesionDeleteView(LoginRequiredMixin, FichaKinesicaMixin, DeleteView):
    model = Sesion

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk_sesion', None)
        self.object = Sesion.objects.get(pk=pk)
        return self.object

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS,
                             "La sesión fue eliminada correctamente.")
        return reverse('turno_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())



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
tratamiento_list = TratamientoListView.as_view()
tratamiento_create = TratamientoAddView.as_view()
tratamiento_update = TratamientoEditView.as_view()
objetivo_update = ObjetivoEditView.as_view()
sesion_create = SesionCreateView.as_view()
sesion_save_close = SesionSaveAndCloseView.as_view()
sesion_delete = SesionDeleteView.as_view()
# planificacion_create = PlanificacionCreateView.as_view()