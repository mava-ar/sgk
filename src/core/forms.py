from django import forms
from django.conf import settings

from datetimewidget.widgets import DateWidget

from dj_utils.fields import FechaField
from core.models import Persona, Contacto


class PersonaForm(forms.ModelForm):
    fecha_nacimiento = FechaField(initial="01/01/1980")

    class Meta:
        model = Persona
        fields = ('nombre', 'apellido', 'dni', 'fecha_nacimiento', 'genero', 'estado_civil',
                  'domicilio', 'profesion', 'imagen_perfil', )


class ContactoForm(forms.ModelForm):

    class Meta:
        model = Contacto
        fields = ('telefono', 'celular', 'notificar_sms', 'email', 'horario')
