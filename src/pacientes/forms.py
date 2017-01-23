from django import forms

from dj_utils.fields import FechaField
from coberturas_medicas.models import Cobertura
from pacientes.models import Antecedente, Paciente


class PacienteForm(forms.ModelForm):
    particular = forms.BooleanField(required=False, initial=True, label='Particular')
    cobertura_medica = forms.ModelChoiceField(Cobertura.objects.all(), required=False, empty_label='')
    fecha_ingreso = FechaField()

    class Meta:
        model = Paciente
        fields = ('fecha_ingreso', 'particular', 'cobertura_medica', 'observaciones')

    def __init__(self, **kwargs):
        super(PacienteForm, self).__init__(**kwargs)
        if self.instance:
            self.initial["particular"] = True if self.instance.cobertura_medica_id == Cobertura.objects.get_particular().pk else False

    def clean(self):
        cleaned_data = super(PacienteForm, self).clean()
        if cleaned_data["particular"]:
            cleaned_data["cobertura_medica"] = None
        else:
            if cleaned_data["cobertura_medica"] is None:
                self.add_error('particular', 'Debe indicar si tiene cobertura médica o si se atiende de forma particular')

    def save(self, commit=True):
        saved = super(PacienteForm, self).save(commit=False)
        if self.cleaned_data["particular"]:
            saved.cobertura_medica = Cobertura.objects.get_particular()
        if commit:
            saved.save()
        return saved


class AntecedenteForm(forms.ModelForm):
    menarca = forms.DateField(required=False)
    fum = forms.DateField(required=False)

    class Meta:
        model = Antecedente
        fields = ('patologicos', 'quirurgicos', 'traumaticos', 'alergicos',
                  'heredo_familiar', 'habitos_fisiologicos', 'actividad_fisica',
                  'habitos_patologicos', 'medicaciones', 'estudios_complementarios',
                  'menarca', 'fum', 'tipo_partos', 'observaciones')