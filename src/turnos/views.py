import dateutil.parser

from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView, CreateView, UpdateView
from django.shortcuts import render

from dj_utils.mixins import TableFilterListView
from turnos.forms import TurnoForm, TurnoDeleteForm
from turnos.models import Turno
from turnos.tables import TurnosReporteTable
from turnos.filters import TurnosReportFilter
from tratamientos.forms import SesionPerdidaForm


class TurnosListView(LoginRequiredMixin, TemplateView):
    template_name = "turnos/turno_list.html"


class TurnoCreateView(LoginRequiredMixin, CreateView):
    model = Turno
    form_class = TurnoForm

    def dispatch(self, *args, **kwargs):
        try:
            self.request.user.profesional
        except ObjectDoesNotExist:
            return render(self.request, 'mensajes/turno_no_profesional.html')
        return super(TurnoCreateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(TurnoCreateView, self).get_context_data(**kwargs)
        if self.request.GET.get("time", False):
            ctx["form"].initial["hora"] = dateutil.parser.parse(self.request.GET.get("time"))
            ctx["form"].initial["dia"] = dateutil.parser.parse(self.request.GET.get("time"))
        return ctx

    def form_valid(self, form):
        turno = form.save(commit=False)
        turno.profesional = self.request.user.profesional
        turno.save()
        return render(self.request, 'mensajes/turno_saved.html')


class TurnoEditView(TurnoCreateView, UpdateView):

    def dispatch(self, *args, **kwargs):
        return super(UpdateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(TurnoEditView, self).get_context_data(**kwargs)
        ctx["delete_form"] = TurnoDeleteForm(instance=ctx["object"])
        return ctx

    def form_valid(self, form):
        turno = form.save(commit=False)
        turno.save()
        return self.then_save(turno)

    def then_save(self, turno):
        try:
            self.request.user.profesional
            if settings.PLAN_KINES > 1 and (
                turno.paciente and turno.paciente.tratamiento_activo()) and all(
                    (turno.sesion is None, turno.no_asistio, turno.no_aviso)):
                return render(self.request, 'turnos/sesion_perdida.html', {
                    'turno': turno, 'form': SesionPerdidaForm()})
        except ObjectDoesNotExist:
            pass
        return render(self.request, 'mensajes/turno_saved.html')

    def get_template_names(self):
        if settings.PLAN_KINES == 2:
            return ["turnos/turno_form_plan2.html"]
        return ["turnos/turno_form.html"]


class TurnoDeleteView(LoginRequiredMixin, UpdateView):
    model = Turno
    http_method_names = ["post", ]

    def post(self, request, *args, **kwargs):
        form = TurnoDeleteForm(request.POST, instance=self.get_object())
        if form.is_valid():
            form.instance.delete()
        return render(self.request, 'mensajes/turno_delete.html', {'success': form.is_valid()})


class TurnosInformesView(TableFilterListView):
    table_class = TurnosReporteTable
    filterset_class = TurnosReportFilter
    template_name = "turnos/turno_report.html"
    queryset = Turno.objects.all().order_by('-dia', 'hora')


turno_list = TurnosListView.as_view()
turno_create = TurnoCreateView.as_view()
turno_update = TurnoEditView.as_view()
turno_delete = TurnoDeleteView.as_view()
turno_report = TurnosInformesView.as_view()