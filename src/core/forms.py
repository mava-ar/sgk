from datetime import datetime

from django import forms
from django.forms.widgets import SelectDateWidget

from core.models import Persona, Contacto


class PersonaForm(forms.ModelForm):

    class Meta:
        model = Persona
        fields = ('nombre', 'apellido', 'dni', 'fecha_nacimiento', 'genero', 'estado_civil',
                  'domicilio', 'profesion', 'imagen_perfil', )
        widgets = {
            'fecha_nacimiento': SelectDateWidget(years=range(1900, datetime.now().year))
        }


class ContactoForm(forms.ModelForm):

    class Meta:
        model = Contacto
        fields = ('telefono', 'celular', 'notificar_sms', 'email', 'horario')
