from django import forms
from django.forms import inlineformset_factory

from dj_utils.fields import FechaField
from .models import MotivoConsulta, Objetivo


class MotivoConsultaForm(forms.ModelForm):
    paciente = forms.HiddenInput()

    class Meta:
        model = MotivoConsulta
        fields = ('motivo_consulta_paciente', 'diagnostico_medico',
                  'evaluacion_kinesica', 'tratamientos_previos', 'observaciones')


class ObjetivoInlineForm(forms.ModelForm):
    fecha_inicio = FechaField(required=False)
    fecha_cumplido = FechaField(required=False)

    class Meta:
        model = Objetivo
        fields = ('descripcion', 'fecha_inicio', 'fecha_cumplido', 'observaciones')


ObjetivoInlineFormset = inlineformset_factory(MotivoConsulta, Objetivo, form=ObjetivoInlineForm, extra=1)