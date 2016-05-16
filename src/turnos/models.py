from django.db import models

from dj_utils.models import BaseModel
from core.models import Profesional
from pacientes.models import Paciente
from coberturas_medicas.models import Cobertura
from tratamientos.models import Sesion


class Turno(BaseModel):
    """
    Reservación de un turno para una sesión en el consultorio.
    """
    dia = models.DateField('día')
    hora = models.TimeField('hora')
    duracion = models.PositiveSmallIntegerField('duración', default=60,
            help_text="duración en minutos de la sesión.")
    motivo = models.CharField('motivo', max_length=255, blank=True)
    asistio = models.BooleanField('¿asistió?', default=False)
    aviso = models.BooleanField('¿avisó?', default=False)
    observaciones = models.TextField('observaciones',  blank=True)
    nombre_paciente = models.CharField('nombre del paciente', max_length=255, blank=True,
            help_text='Dejar en blanco si el paciente se encuentra en el sistema.')

    # relaciones
    profesional = models.ForeignKey(Profesional, verbose_name='profesional')
    paciente = models.ForeignKey(Paciente, verbose_name='paciente', null=True)
    cobertura = models. ForeignKey(Cobertura, verbose_name='cobertura', null=True)

    sesion = models.OneToOneField(Sesion, on_delete=models.SET_NULL, verbose_name="sesión realizada", null=True,
                                  related_name='turno_dado')

    def __str__(self):
        nombre = ''
        if self.nombre_paciente:
            nombre = self.nombre_paciente
        # elif self.paciente and self.paciente.persona:
        #     nombre = self.paciente.persona.nombre
        else:
            nombre = "NN"
        return "{} - {} {} ({})".format(nombre, self.dia, self.hora,
                                        self.profesional.persona.nombre)

    class Meta:
        verbose_name = "turno"
        verbose_name_plural = "turnos"
