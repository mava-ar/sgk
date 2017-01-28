from datetime import date

from django.core.files.storage import get_storage_class
from django.conf import settings
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
    celular = models.CharField('celular', max_length=255, blank=True, help_text="Sin guiones ni espacios.")

    email = models.EmailField('e-mail', blank=True)
    horario = models.CharField('horario de contacto', max_length=255, blank=True)
    observaciones = models.TextField('observaciones', blank=True)

    # notificaciones
    notificar_sms = models.BooleanField('notificar por SMS', default=True)

    class Meta:
        verbose_name = u"contacto"
        verbose_name_plural = u"contactos"

    def __str__(self):
        return u"{} {}".format(
                self.nombre, self.apellido)

    def get_basic_info(self):
        info = []
        if self.telefono:
            info.append('Tel: {}'.format(self.telefono))
        if self.celular:
            info.append('Cel: {}'.format(self.celular))
        if self.email:
            info.append('Email: {}'.format(self.email))
        return info


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
        ordering = ('nombre', 'apellido', )
        verbose_name = "persona"
        verbose_name_plural = "personas"

    @property
    def edad(self):
        today = date.today()
        return today.year - self.fecha_nacimiento.year - (
            (today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))

    @property
    def avatar(self):
        return self._avatar("50x50")

    @property
    def avatar_lg(self):
        return self._avatar("250x250")

    def _avatar(self, size):
        if self.imagen_perfil:
            img = self.imagen_perfil["avatar"].url
        else:
            static_storage = get_storage_class(settings.STATICFILES_STORAGE)()
            if self.genero == 'F':
                img = static_storage.url("img/icons/{}/mujer.png".format(size))
            elif self.genero == 'M':
                img = static_storage.url("img/icons/{}/hombre.png".format(size))
            else:
                img = static_storage.url("img/icons/{}/desconocido.png".format(size))
        return img


class Profesional(BaseModel):
    """
    Profesional que trabaja en el lugar,
    el cual puede tomar turnos y pacientes.

    """
    titulo = models.CharField("título", max_length=64, blank=True, help_text="Ej: Lic.")
    persona = models.OneToOneField(Persona, verbose_name='persona')
    usuario = models.OneToOneField(User, verbose_name='usuario', null=True)
    observaciones = models.TextField('observaciones', blank=True)

    def __str__(self):
        if self.titulo:
            return "{} {}".format(self.titulo, self.persona.nombre)
        return "{}".format(self.persona.nombre)

    class Meta:
        verbose_name = "profesional"
        verbose_name_plural = "profesionales"
