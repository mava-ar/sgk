from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from coberturas_medicas.managers import CoberturaManager
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
    cobertura_propia = models.BooleanField(verbose_name='cobertura propia', default=False,
                                           help_text='No es una cobertura, sino el pago del servicio por el particular')
    paga_por_sesion = models.BooleanField(
        verbose_name="paga por sesión", default=False,
        help_text="Seleccionar para indicar que la cobertura paga cada sesión individualmente.")

    # contacto = models.ManyToOneRel(Contacto, verbose_name=u'Contacto', null=True, related_name='obrasocial')

    objects = CoberturaManager()

    def __str__(self):
        if self.codigo:
            return "{} ({})".format(self.nombre, self.codigo)
        return self.nombre

    class Meta:
        ordering = ('nombre', )
        verbose_name = "cobertura médica"
        verbose_name_plural = "coberturas médicas"

    def clean(self):
        if self.cobertura_propia:
            others = self.objects.filter(cobertura_propia=True)
            if (self.pk and others.exclude(pk=self.pk).exists()) or (self.pk is None and others.exists()):
                raise ValidationError('Sólo es posible una sóla cobertura particular.')


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
