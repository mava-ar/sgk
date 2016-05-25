from datetime import timedelta

from django import forms
from django.conf import settings
from django.forms.models import ModelForm, BaseInlineFormSet
from django.utils import timezone

from datetimewidget.widgets import DateWidget, TimeWidget

from dj_utils.fields import FechaField
from .models import Turno
from pacientes.models import Paciente


class TurnoForm(ModelForm):
    paciente = forms.ModelChoiceField(Paciente.objects.all(), required=False)
    dia = FechaField()
    hora = forms.TimeField(widget=TimeWidget(options={"minuteStep": 15, "maxView": 0}, usel10n=True, bootstrap_version=3))
    duracion = forms.IntegerField(widget=forms.HiddenInput(), initial=60)

    class Meta:
        model = Turno
        fields = ('dia', 'hora', 'duracion', 'motivo', 'observaciones',
                  'nombre_paciente', 'paciente', 'profesional', )

    def __init__(self, **kwargs):
        super(TurnoForm, self).__init__(**kwargs)
        hoy = timezone.now()
        hoy = hoy.replace(hour=16, minute=0, second=0, microsecond=0)
        self.initial["hora"] = hoy
        self.initial["dia"] = hoy + timedelta(days=1)
