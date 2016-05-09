from django.db import models


class BaseModel(models.Model):
    """
    Todos los modelos deben heredar de esta clase.

    """
    class Meta:
        abstract = True

    creado_el = models.DateTimeField(verbose_name=u"Fecha de creación",
            auto_now_add=True)
    modificado_el = models.DateTimeField(verbose_name=u"Fecha de modificación",
            auto_now=True)
