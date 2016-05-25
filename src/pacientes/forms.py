from django import forms
from django.conf import settings

from datetimewidget.widgets import DateWidget

from coberturas_medicas.models import Cobertura
from pacientes.models import Antecedente, Paciente


class PacienteForm(forms.ModelForm):
    cobertura = forms.ModelChoiceField(Cobertura.objects.all(), required=False)
    fecha_ingreso = forms.DateField(widget=DateWidget(usel10n=True, bootstrap_version=3),
                                    input_formats=settings.DATE_INPUT_FORMATS)

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