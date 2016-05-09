from django import forms
from django.conf import settings
from django.forms.models import ModelForm, BaseInlineFormSet

from datetimewidget.widgets import DateWidget, TimeWidget

from .models import Turno
from pacientes.models import Paciente


class TurnoForm(ModelForm):
    paciente = forms.ModelChoiceField(Paciente.objects.all(), required=False)
    dia = forms.DateField(
        widget=DateWidget(usel10n=True, bootstrap_version=3, options={"format": "dd/mm/yyyy"}),
        input_formats=settings.DATE_INPUT_FORMATS)
    hora = forms.TimeField(
        widget=TimeWidget(options={"format": "HH:ii"}, usel10n=True, bootstrap_version=3),
        initial="16:00")
    duracion = forms.IntegerField(widget=forms.HiddenInput(), initial=60)

    class Meta:
        model = Turno
        fields = ('dia', 'hora', 'duracion', 'motivo', 'observaciones',
                  'nombre_paciente', 'paciente', 'profesional', )