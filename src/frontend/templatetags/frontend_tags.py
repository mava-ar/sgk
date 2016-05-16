import time
from django import template
from django.utils import timezone
from django.utils.safestring import mark_safe

from sgk.settings.base import STATIC_URL

register = template.Library()


@register.filter(name="profile_image")
def profile_image(persona, config='avatar'):
    if persona.imagen_perfil:
        img = persona.imagen_perfil[config].url
    else:
        if persona.genero == 'F':
            img = STATIC_URL + "img/icons/50x50/mujer.png"
        elif persona.genero == 'M':
            img = STATIC_URL + "img/icons/50x50/hombre.png"
        else:
            img = STATIC_URL + "img/icons/50x50/desconocido.png"
    return img


@register.filter(name="split")
def split(str, splitter):
    return str.split(splitter)


@register.inclusion_tag("tags/show_info.html")
def show_info(data):
    return {
        'data': data.show_info
    }

@register.filter(name="date_to_millis")
def date_to_millis(d):
    d = timezone.localtime(d)
    for_js = int(time.mktime(d.timetuple())) * 1000
    return for_js