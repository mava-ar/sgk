# coding=utf-8
from django.views.generic import TemplateView
from django.utils.timezone import now

from django_weasyprint import PDFTemplateResponseMixin

from dj_utils.mixins import FichaKinesicaConHistoriaMixin


class HistoriaClinicaReportPDFView(FichaKinesicaConHistoriaMixin, PDFTemplateResponseMixin, TemplateView):
    """
    Imprime un pdf con la historia clínica del paciente.

    """
    HISTORIA_CLINICA_COMPLETE = True
    template_name = 'pacientes/historia_clinica_report.html'

    def get_filename(self):
        return u'HISTORIA_CLINICA_%s_(%s).pdf' % (str(self.paciente).upper(), now().strftime("%Y-%m-%d"))

    def get_context_data(self, **kwargs):
        context = super(HistoriaClinicaReportPDFView, self).get_context_data(**kwargs)
        return context


historia_clinica_report_pdf = HistoriaClinicaReportPDFView.as_view()
