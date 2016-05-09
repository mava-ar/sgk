from django import forms
from django.conf import settings

from datetimewidget.widgets import DateWidget

from core.models import Persona, Contacto


class PersonaForm(forms.ModelForm):
    fecha_nacimiento = forms.DateField(widget=DateWidget(
        usel10n=True, bootstrap_version=3), initial="01/01/1980", input_formats=settings.DATE_INPUT_FORMATS)

    class Meta:
        model = Persona
        fields = ('nombre', 'apellido', 'dni', 'fecha_nacimiento', 'genero', 'estado_civil',
                  'domicilio', 'imagen_perfil')


class ContactoForm(forms.ModelForm):

    class Meta:
        model = Contacto
        fields = ('telefono', 'celular', 'email', 'horario')