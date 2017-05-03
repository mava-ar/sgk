# coding=utf-8
from django.views.generic import TemplateView
from django.utils.timezone import now
from django.utils.text import slugify

from dj_utils.mixins import FichaKinesicaConHistoriaMixin
from dj_utils.views import PDFResponseMixin


class HistoriaClinicaReportPDFView(FichaKinesicaConHistoriaMixin, PDFResponseMixin, TemplateView):
    """
    Imprime un pdf con la historia clínica del paciente.

    """
    HISTORIA_CLINICA_COMPLETE = True
    template_name = 'pacientes/historia_clinica_report.html'

    def get_filename(self):
        return "{}.pdf".format(slugify('Historia clínica de {} ({:%Y-%m-%d})'.format(self.paciente, now())))

    def get_context_data(self, **kwargs):
        context = super(HistoriaClinicaReportPDFView, self).get_context_data(**kwargs)
        return context


historia_clinica_report_pdf = HistoriaClinicaReportPDFView.as_view()
