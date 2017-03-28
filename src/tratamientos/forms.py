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
    cumplido = forms.BooleanField(label='Objetivo cumplido', required=False)

    class Meta:
        model = Objetivo
        fields = ('descripcion', 'observaciones', 'cumplido')

    def __init__(self, **kwargs):
        super(ObjetivoForm, self).__init__(**kwargs)
        if self.instance:
            self.initial["cumplido"] = self.instance.fecha_cumplido is not None

    def save(self, commit=True):
        if "cumplido" in self.cleaned_data and self.cleaned_data["cumplido"]:
            fecha_cumplido = timezone.now()
            del self.cleaned_data["cumplido"]
        else:
            fecha_cumplido = None
        instance = super(ObjetivoForm, self).save(commit=False)
        instance.fecha_cumplido = fecha_cumplido
        if commit:
            instance.save()
        return instance


ObjetivoInlineFormset = inlineformset_factory(MotivoConsulta, Objetivo, form=ObjetivoForm, extra=1, can_delete=True)


class ObjetivoCumplidoUpdateForm(forms.ModelForm):

    class Meta:
        model = Objetivo
        fields = ('id', )


class PlanificacionCreateForm(forms.ModelForm):
    class Meta:
        model = Planificacion
        fields = ('por_sesion', 'cantidad_sesiones', 'frecuencia', 'comentarios', )


class PlanificacionFinishForm(forms.ModelForm):
    motivo_finalizacion = forms.CharField(
        label='Motivo de finalización', required=True,
        help_text='Comente un motivo por el cual finaliza el tratamiento de forma anticipada.')

    class Meta:
        model = Planificacion
        fields = ('motivo_finalizacion', )

    def save(self, commit=True):
        instance = super(PlanificacionFinishForm, self).save(commit=False)
        instance.estado = Planificacion.FINALIZADO
        if commit:
            instance.save()
        return instance


class NuevaSesionForm(forms.ModelForm):
    fecha = FechaField(label="fecha de la sesión", initial=timezone.now())

    class Meta:
        model = Sesion
        fields = ('fecha', 'duracion', 'estado_paciente', 'actividad', 'comentarios', )


class SesionUpdateForm(forms.ModelForm):

    class Meta:
        model = Sesion
        fields = ('estado_paciente', 'actividad', 'comentarios', )


class SesionPerdidaForm(forms.ModelForm):

    class Meta:
        model = Sesion
        fields = ('comentarios', )

    def __init__(self, **kwargs):
        super(SesionPerdidaForm, self).__init__(**kwargs)
        self.initial["comentarios"] = "Paciente ausente, sesión perdida"
