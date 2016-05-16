from django import forms
from django.forms import inlineformset_factory
from django.utils import timezone

from dj_utils.fields import FechaField
from .models import MotivoConsulta, Objetivo, Planificacion, Sesion


class MotivoConsultaForm(forms.ModelForm):
    paciente = forms.HiddenInput()

    class Meta:
        model = MotivoConsulta
        fields = ('motivo_consulta_paciente', 'diagnostico_medico',
                  'evaluacion_kinesica', 'tratamientos_previos', 'observaciones')


class ObjetivoForm(forms.ModelForm):

    class Meta:
        model = Objetivo
        fields = ('descripcion', 'observaciones')


ObjetivoInlineFormset = inlineformset_factory(MotivoConsulta, Objetivo, form=ObjetivoForm, extra=1)


class ObjetivoCumplidoUpdateForm(forms.ModelForm):
    class Meta:
        model = Objetivo
        fields = ('fecha_cumplido', )
        widgets = {
            'fecha_cumplido': forms.HiddenInput()
        }


class PlanificacionCreateForm(forms.ModelForm):
    class Meta:
        model = Planificacion
        fields = ('cantidad_sesiones', 'frecuencia', 'comentarios', )


class NuevaSesionForm(forms.ModelForm):
    fecha = FechaField(label="fecha de la sesión", initial=timezone.now())

    class Meta:
        model = Sesion
        fields = ('fecha', 'duracion', 'estado_paciente', 'actividad', 'comentarios', )