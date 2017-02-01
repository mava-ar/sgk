import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db.transaction import atomic
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils import html, timezone
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from dj_utils.mixins import FichaKinesicaMixin
from tratamientos.forms import (ObjetivoForm, MotivoConsultaForm, ObjetivoInlineFormset,
                                PlanificacionCreateForm, NuevaSesionForm, ObjetivoCumplidoUpdateForm,
                                SesionUpdateForm, SesionPerdidaForm)
from tratamientos.models import MotivoConsulta, Objetivo, Planificacion, Sesion
from turnos.models import Turno


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
        if self.paciente.motivos_de_consulta.filter(planificaciones__estado__in=Planificacion.estados_activos()):
            messages.add_message(
                self.request, messages.ERROR, "Existe un tratamiento en curso en este momento. "
                                              "Finalicelo antes de iniciar otro.")
            return HttpResponseRedirect(
                reverse('tratamiento_list', kwargs={'pk': self.paciente.pk}))
        return super(TratamientoAddView, self).get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(TratamientoAddView, self).get_context_data(*args, **kwargs)
        if "objetivo_formset" not in context:
            context['objetivo_formset'] = ObjetivoInlineFormset(self.request.POST) if self.request.POST else ObjetivoInlineFormset()
        if "tratamiento_form" not in context:
            context["tratamiento_form"] = PlanificacionCreateForm(self.request.POST) if self.request.POST else PlanificacionCreateForm()
        return context

    def post(self, request, *args, **kwargs):
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
        self.object = None
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
        return self.render_to_response(self.get_context_data(
            form=form, objetivo_formset=objetivo_formset, tratamiento_form=tratamiento_form))

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

    def get_context_data(self, *args, **kwargs):
        context = super(TratamientoEditView, self).get_context_data(*args, **kwargs)
        if "objetivo_formset" not in context:
            context['objetivo_formset'] = ObjetivoInlineFormset(instance=self.object)
        if "tratamiento_form" not in context:
            context["tratamiento_form"] = PlanificacionCreateForm(instance=self.object.planificaciones.last())
        return context

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
        form.save()
        objetivo_formset.save()
        tratamiento_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, objetivo_formset, tratamiento_form):
        return self.render_to_response(self.get_context_data(
            form=form, objetivo_formset=objetivo_formset, tratamiento_form=tratamiento_form))

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS,
                             "Tratamiento actualizado correctamente.")
        return reverse('tratamiento_list', kwargs={'pk': self.paciente.pk})


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


class ObjetivoToggleCheckView(LoginRequiredMixin, FichaKinesicaMixin, UpdateView):
    model = Objetivo
    form_class = ObjetivoCumplidoUpdateForm

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk_objetivo', None)
        self.object = Objetivo.objects.get(pk=pk)
        return self.object

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(ObjetivoToggleCheckView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ObjetivoCumplidoUpdateForm(request.POST)
        status = 'error'
        if form.is_valid():
            self.object.fecha_cumplido = timezone.now() if self.object.fecha_cumplido is None else None
            self.object.save()
            status = 'success'
        context = RequestContext(request)
        context.update({'objetivo': self.object, 'paciente': self.get_paciente()})
        return HttpResponse(json.dumps(
            {
                'html': render_to_string('tratamientos/includes/objectivo_inline.html', context),
                'status': status
            }), content_type='application/json')


class SesionCreateView(LoginRequiredMixin, FichaKinesicaMixin, UpdateView):
    model = Sesion
    form_class = NuevaSesionForm
    template_name = "frontend/sesion_form.html"

    def check_turno(self):
        """
        Este método intenta asociar un turno con la sesión. Si se inicia sesión desde turnos, esto se
        hará mediante el parametro en la url. Sino, se intenta buscando turnos del paciente para hoy,
        que no tengan una sesión asociada.
        """
        try:
            self.object.turno_dado
        except Turno.DoesNotExist:
            turno_pk = self.request.GET.get('turno', None)
            if turno_pk:
                turno = Turno.objects.get(pk=turno_pk)
            else:
                turno = Turno.objects.filter(
                    paciente=self.paciente, dia=timezone.now(), sesion__isnull=True).first()
            if turno:
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
        return reverse('tratamiento_list', kwargs={'pk': self.paciente.pk})

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
        return reverse('tratamiento_list', kwargs={'pk': self.paciente.pk })

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())


class SesionUpdateView(LoginRequiredMixin, FichaKinesicaMixin, UpdateView):
    model = Sesion
    form_class = SesionUpdateForm
    template_name = "frontend/sesion_update_form.html"

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk_sesion', None)
        self.object = Sesion.objects.get(pk=pk)
        return self.object

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS,
                             "La sesión fue actualizada correctamente.")
        return reverse('tratamiento_list', kwargs={'pk': self.paciente.pk })


class SesionPerdidaCreateView(LoginRequiredMixin, FichaKinesicaMixin, CreateView):
    model = Sesion
    http_method_names = ["post", ]

    def post(self, request, *args, **kwargs):
        turno = get_object_or_404(Turno, pk=kwargs.get('pk_turno'))
        self.object = Sesion(paciente=self.paciente)
        form = SesionPerdidaForm(data=request.POST, instance=self.object)
        self.object = form.save(commit=False)
        self.object.motivo_consulta = self.object.paciente.tratamiento_activo()
        self.object.fecha = timezone.now().today()
        self.object.fin_el = timezone.now()
        self.object.save()
        turno.sesion = self.object
        turno.save()
        return render(self.request, 'mensajes/sesion_perdida_ok.html')


tratamiento_list = TratamientoListView.as_view()
tratamiento_create = TratamientoAddView.as_view()
tratamiento_update = TratamientoEditView.as_view()
objetivo_update = ObjetivoEditView.as_view()
objetivo_cumplido_toggle = ObjetivoToggleCheckView.as_view()
sesion_create = SesionCreateView.as_view()
sesion_perdida_create = SesionPerdidaCreateView.as_view()
sesion_save_close = SesionSaveAndCloseView.as_view()
sesion_delete = SesionDeleteView.as_view()
sesion_update = SesionUpdateView.as_view()
