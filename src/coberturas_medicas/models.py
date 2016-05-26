from django.db import models
from django.utils import timezone

from dj_utils.models import BaseModel


class Cobertura(BaseModel):
    """
    Representa una obra social o mutual.

    """
    nombre = models.CharField('nombre', max_length=255)
    codigo = models.CharField('código', max_length=255, blank=True)
    telefono = models.CharField('teléfono', max_length=25, blank=True)
    direccion = models.CharField('dirección', max_length=255, blank=True)
    fax = models.CharField('fax', max_length=25, blank=True)
    email = models.EmailField('email', blank=True)

    activo = models.BooleanField(verbose_name='activo', default=True)

    paga_por_sesion = models.BooleanField(
        verbose_name="paga por sesión", default=False,
        help_text="Seleccionar para indicar que la cobertura paga cada sesión individualmente.")
    # contacto = models.ManyToOneRel(Contacto, verbose_name=u'Contacto', null=True, related_name='obrasocial')

    def __str__(self):
        return "{}".format(self.nombre)

    class Meta:
        verbose_name = "cobertura médica"
        verbose_name_plural = "coberturas médicas"


class RegistroValorPrestacion(BaseModel):
    """
    Valor pagado por la cobertura para una sesión de kinesionloǵia.
    """
    cobertura = models.ForeignKey(Cobertura, related_name="valores")
    monto = models.DecimalField('monto ($)', max_digits=8, decimal_places=2)
    fecha_baja = models.DateTimeField('fecha de baja', null=True, blank=True,
                                      help_text="Si la fecha está vacia, el valor es el vigente. "
                                                "Será establecido automáticamente al ingresar un nuevo valor")

    def __str__(self):
        return "{0} - ${1:0.2f}".format(self.cobertura, self.monto)

    class Meta:
        verbose_name_plural = 'valores de prestación'
        verbose_name = 'valor de prestación'
        
    def save(self, **kwargs):
        """
        Al guardar, verificar si existe otro valor de la misma cobertura vigente, e invalidarlo.
        """
        qs = RegistroValorPrestacion.objects.filter(cobertura=self.cobertura, fecha_baja__isnull=True)
        if self.pk:
            qs.exclude(pk=self.pk)
        qs.update(fecha_baja=timezone.now())
        super(RegistroValorPrestacion, self).save(**kwargs)
