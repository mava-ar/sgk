from django import forms

from dj_utils.fields import FechaField
from coberturas_medicas.models import Cobertura
from pacientes.models import Antecedente, Paciente


class PacienteForm(forms.ModelForm):
    cobertura = forms.ModelChoiceField(Cobertura.objects.all(), required=False, empty_label='')
    fecha_ingreso = FechaField()

    class Meta:
        model = Paciente
        fields = ('fecha_ingreso', 'cobertura', 'observaciones')


class AntecedenteForm(forms.ModelForm):
    menarca = forms.DateField(required=False)
    fum = forms.DateField(required=False)

    class Meta:
        model = Antecedente
        fields = ('patologicos', 'quirurgicos', 'traumaticos', 'alergicos',
                  'heredo_familiar', 'habitos_fisiologicos', 'actividad_fisica',
                  'habitos_patologicos', 'medicaciones', 'estudios_complementarios',
                  'menarca', 'fum', 'tipo_partos', 'observaciones')