from django.forms import DateField

from dj_utils.widgets import FechaWidget
from sgk.settings.base import DATE_INPUT_FORMATS


class FechaField(DateField):
    """
    Configura un DateField con el formato de fecha y widget correcto.
    """
    def __init__(self, *args, **kwargs):
        kwargs.update({"widget": FechaWidget})
        kwargs.update({"input_formats": DATE_INPUT_FORMATS})
        super(FechaField, self).__init__(*args, **kwargs)
