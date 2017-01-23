from django import forms

from dj_utils.fields import FechaField
from coberturas_medicas.models import Cobertura
from pacientes.models import Antecedente, Paciente


class PacienteForm(forms.ModelForm):
    particular = forms.BooleanField(required=False, initial=True, label='Particular')
    cobertura_medica = forms.ChoiceField(choices=Cobertura.objects.none(), required=False, initial='')
    nueva_cobertura = forms.CharField(label='Nueva cobertura', required=False)
    fecha_ingreso = FechaField()

    class Meta:
        model = Paciente
        fields = ('fecha_ingreso', 'particular', 'cobertura_medica', 'nueva_cobertura', 'observaciones')

    def __init__(self, **kwargs):
        super(PacienteForm, self).__init__(**kwargs)
        self.fields["cobertura_medica"].choices = [(-1, "Nueva cobertura")] + [(x.pk, str(x)) for x in Cobertura.objects.all()]
        if self.instance:
            self.initial["particular"] = True if self.instance.cobertura_medica_id == Cobertura.objects.get_particular().pk else False

    def clean(self):
        cleaned_data = super(PacienteForm, self).clean()
        if cleaned_data["particular"]:
            cleaned_data["cobertura_medica"] = None
            cleaned_data["nueva_cobertura"] = ''
        elif cleaned_data["cobertura_medica"] != '-1':
            cleaned_data["cobertura_medica"] = Cobertura.objects.get(pk=cleaned_data["cobertura_medica"])
            cleaned_data["nueva_cobertura"] = ''
        else:
            cleaned_data["cobertura_medica"] = None  # siempre debo hacer None si es -1
            if cleaned_data["nueva_cobertura"] == '':
                self.add_error('nueva_cobertura', 'Por favor, ingrese el nombre de la nueva cobertura médica')

    def save(self, commit=True):
        saved = super(PacienteForm, self).save(commit=False)
        if self.cleaned_data["particular"]:
            saved.cobertura_medica = Cobertura.objects.get_particular()
        if self.cleaned_data["nueva_cobertura"] != '':
            saved.cobertura_medica = Cobertura.objects.create(nombre=self.cleaned_data["nueva_cobertura"])
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