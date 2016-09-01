from django.contrib.auth.models import User
from django.db import models

from easy_thumbnails.fields import ThumbnailerImageField

from dj_utils.models import BaseModel


class Contacto(BaseModel):
    """
    Representa un contacto.

    Puede ser los datos de contacto de un paciente, un profesional,
    o otra persona relacionado con el sistema.

    """
    nombre = models.CharField('nombre', max_length=255, blank=True)
    apellido = models.CharField('npellido', max_length=255, blank=True)
    telefono = models.CharField('teléfono', max_length=255, blank=True)
    celular = models.CharField('celular', max_length=255, blank=True)
    email = models.EmailField('e-mail', blank=True)
    horario = models.CharField('horario de contacto', max_length=255, blank=True)
    observaciones = models.TextField('observaciones', blank=True)

    class Meta:
        verbose_name = u"contacto"
        verbose_name_plural = u"contactos"

    def __str__(self):
        return u"{} {}".format(
                self.nombre, self.apellido)


class Persona(BaseModel):
    """
    Una persona del sistema.

    Contiene los datos de un paciente, un profesional
    o cualquier otra persona.

    """
    GENERO = (
        ('F', 'Femenino'),
        ('M', 'Masculino'),
        ('O', 'Otro')
    )
    ESTADO_CIVIL = (
        ('S', "Soltero"),
        ('C', "Casado"),
        ('D', "Divorciado"),
        ('V', "Viudo"),
        ('CV', "Concuvinato")
    )
    nombre = models.CharField('nombre', max_length=255)
    apellido = models.CharField('apellido', max_length=255)
    fecha_nacimiento = models.DateField('fecha de nacimiento', null=True)
    genero = models.CharField('género', max_length=1, choices=GENERO, default='F')
    estado_civil = models.CharField('estado civíl', max_length=3, choices=ESTADO_CIVIL, default='S')
    dni = models.IntegerField('DNI', null=True, blank=True)
    domicilio = models.CharField('domicilio', max_length=255, blank=True)
    imagen_perfil = ThumbnailerImageField(upload_to='imagen_perfil', blank=True, null=True)
    observaciones = models.TextField('observaciones', blank=True)
    # relaciones
    info_contacto = models.OneToOneField(Contacto, verbose_name='contacto', null=True, blank=True)
    profesion = models.CharField(verbose_name='profesión', null=True, blank=True, max_length=255)

    def __str__(self):
        return "{} {}".format(
                self.nombre, self.apellido)

    class Meta:
        verbose_name = "persona"
        verbose_name_plural = "personas"


class Profesional(BaseModel):
    """
    Profesional que trabaja en el lugar,
    el cual puede tomar turnos y pacientes.

    """
    persona = models.OneToOneField(Persona, verbose_name='persona')
    usuario = models.OneToOneField(User, verbose_name='usuario', null=True)
    observaciones = models.TextField('observaciones', blank=True)

    def __str__(self):
        return "{}".format(
                self.persona.nombre)

    class Meta:
        verbose_name = "profesional"
        verbose_name_plural = "profesionales"
