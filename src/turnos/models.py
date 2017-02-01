from datetime import datetime, timedelta

from django.db import models

from dj_utils.models import BaseModel
from core.models import Profesional
from pacientes.models import Paciente
from coberturas_medicas.models import Cobertura
from tratamientos.models import Sesion


class Turno(BaseModel):
    """
    Reserva de un turno para una sesión en el consultorio.
    """
    dia = models.DateField('día')
    hora = models.TimeField('hora')
    duracion = models.PositiveSmallIntegerField('duración', default=60,
            help_text="duración en minutos de la sesión.")
    motivo = models.CharField('motivo', max_length=255, blank=True)
    no_asistio = models.BooleanField('No asistió', default=False, help_text="Marcar en caso de NO asistencia del paciente.")
    no_aviso = models.BooleanField('No avisó', default=False, help_text="Marcar en caso de NO asistencia sin previo no_aviso.")
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
        elif self.paciente:
            nombre = str(self.paciente)
        else:
            nombre = "NN"
        return "{} - {} {} ({})".format(nombre, self.dia, self.hora, str(self.profesional))

    class Meta:
        verbose_name = "turno"
        verbose_name_plural = "turnos"

    @property
    def title(self):
        return self.paciente.persona.__str__() if self.paciente else self.nombre_paciente

    @property
    def datetime_start(self):
        return datetime.combine(self.dia, self.hora)

    @property
    def datetime_end(self):
        return self.datetime_start + timedelta(minutes=self.duracion)
