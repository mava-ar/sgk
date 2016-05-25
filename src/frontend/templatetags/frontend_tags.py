import time
from django import template
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe

from sgk.settings.base import STATIC_URL

from pacientes.models import ComentariosHistoriaClinica, ImagenesHistoriaClinica

register = template.Library()


@register.filter(name="profile_image")
def profile_image(persona, config='avatar'):
    size = "50x50" if config == 'avatar' else "250x250"
    if persona.imagen_perfil:
        img = persona.imagen_perfil[config].url
    else:
        if persona.genero == 'F':
            img = STATIC_URL + "img/icons/{}/mujer.png".format(size)
        elif persona.genero == 'M':
            img = STATIC_URL + "img/icons/{}/hombre.png".format(size)
        else:
            img = STATIC_URL + "img/icons/{}/desconocido.png".format(size)
    return img


@register.filter(name="split")
def split(str, splitter):
    return str.split(splitter)


@register.inclusion_tag("tags/show_info.html")
def show_info(data):
    return {
        'data': data.show_info
    }


@register.inclusion_tag("tags/entrada_historia_clinica.html")
def show_entry(data, panel_class='info'):
    return {
        'entry': data,
        'data': data.show_info,
        'panel_class': panel_class
    }


@register.filter(name="date_to_millis")
def date_to_millis(d):
    d = timezone.localtime(d)
    for_js = int(time.mktime(d.timetuple())) * 1000
    return for_js


@register.simple_tag
def are_same_date(date1, date2):
    """
    devuelve True si hay mas de 60 segundos de diferencia entre las fechas.
    """
    diff = (date1 - date2).total_seconds()
    return diff > 60 or diff < -60

@register.simple_tag
def get_edit_url_entry(entry):
    # debo determinar
    if isinstance(entry, ComentariosHistoriaClinica):
        return reverse('comentario_hc_update', kwargs={'pk': entry.paciente.pk, 'pk_comentario': entry.pk })
    if isinstance(entry, ImagenesHistoriaClinica):
        return reverse('imagen_hc_update', kwargs={'pk': entry.paciente.pk, 'pk_imagen': entry.pk})
    return ""