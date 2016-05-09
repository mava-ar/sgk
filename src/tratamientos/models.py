from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from pacientes.models import Paciente
from dj_utils.models import BaseModel
from dj_utils.mixins import ShowInfoMixin


class MotivoConsulta(BaseModel, ShowInfoMixin):
    """
    Contiene información sobre el motivo por el cual
    el paciente debe tomar algunas sesiones.

    """
    paciente = models.ForeignKey(Paciente, verbose_name='paciente',
                                 related_name='motivos_de_consulta')
    motivo_consulta_paciente = models.TextField(
            'motivo según el paciente', blank=True, default="",
            help_text="Signos y síntomas explicados por el paciente.")
    diagnostico_medico = models.TextField('diagnóstico médico',
            help_text='Diagnóstico que elaboró el médico especialista.')
    evaluacion_kinesica = models.TextField('evaluación kinésica',
            help_text='Evaluación elaborada por el kinesiólogo/a.')
    tratamientos_previos = models.TextField('tratamientos previos', blank=True,
            help_text='Descripción de tratamientos previos '
                      'por el mismo motivo de consulta')
    observaciones = models.TextField('observaciones', blank=True)

    field_info = ('motivo_consulta_paciente', 'diagnostico_medico',
                  'evaluacion_kinesica', 'tratamientos_previos',
                  'observaciones')

    def __str__(self):
        if self.evaluacion_kinesica:
            return "{} - {}".format(
                self.evaluacion_kinesica[:50], self.creado_el.strftime("%d/%m/%Y"))
        elif self.diagnostico_medico:
            return "{} - {}".format(
                self.diagnostico_medico[:50], self.creado_el.strftime("%d/%m/%Y"))
        else:
            return "{}".format(self.creado_el)

    class Meta:
        verbose_name = u"motivo de consulta"
        verbose_name_plural = u"motivos de consulta"


class Objetivo(BaseModel, ShowInfoMixin):
    """
    Representa un objetivo del tratamiento.
    Puede haber varios para un tratamiento, y se van cumpliendo
    con el paso de las sesiones.

    """
    motivo_consulta = models.ForeignKey(MotivoConsulta,
            verbose_name='motivo de consulta', related_name='objetivos')
    descripcion = models.CharField('descripción', max_length=255)
    fecha_inicio = models.DateField('fecha de inicio', null=True)
    fecha_cumplido = models.DateField('fecha de éxito', null=True)
    observaciones = models.TextField('observaciones', blank=True)

    field_info = ('descripcion', 'fecha_inicio', 'fecha_cumplido', 'observaciones', )

    def __unicode__(self):
        return u"{}".format(self.descripcion)

    class Meta:
        verbose_name = "objectivo"
        verbose_name_plural = "objetivos"


class Planificacion(BaseModel):
    """
    La planificación puede ser diseñada por el profesional, o por el médico especialista
    que indicó sesiones de kinesiología. Contiene la información sobre el tratamiento pensado
    el motivo de consulta relacionado.
    """
    PLANIFICACION_ESTADO = (
        (1, 'Planificado'),
        (2, 'En curso'),
        (3, 'Finalizado'),
        (4, 'Cancelado')
    )
    motivo_consulta = models.ForeignKey(MotivoConsulta, related_name='planificaciones')
    fecha_ingreso = models.DateField('fecha de ingreso', auto_now_add=True)
    fecha_alta = models.DateField('fecha de alta', null=True, blank=True,
            help_text='fecha de alta tentativa.')
    cantidad_sesiones = models.IntegerField(u'cantidad de sesiones',
            help_text='Cantidad de sesiones necesarias recetadas por el médico.', default=10)
    frecuencia = models.PositiveIntegerField(
        'frecuencia semanal', default=1, validators=[MinValueValidator(1), MaxValueValidator(7)])
    estado = models.IntegerField("estado", choices=PLANIFICACION_ESTADO, default=1)
    comentarios = models.TextField("comentarios", blank=True, null=True)
    conclusion = models.TextField("conclusión", blank=True, null=True)

    def __str__(self):
        return "Planificación de {} - {} sesiones - {}".format(
            self.motivo_consulta.paciente, self.cantidad_sesiones, self.estado
        )

    class Meta:
        verbose_name_plural = 'planificaciones'
        verbose_name = 'planificación'


class Sesion(BaseModel):
    """
    Representa una sesión tomada por el paciente. En ella, se indica
    como se encuentra el paciente previamente, que actividades se realizan,
    y la duración.
    """
    paciente = models.ForeignKey(Paciente, related_name='sesiones_paciente')
    motivo_consulta = models.ForeignKey(MotivoConsulta, related_name='sesiones', null=True)
    fecha = models.DateField("fecha")
    duracion = models.PositiveSmallIntegerField("duración de la sesión", default=60,
                                                help_text="Duración de la sesión en minutos")
    estado_paciente = models.TextField(
        "estado de paciente", blank=True, null=True,
        help_text="Descripción de cómo se siente el paciente antes de la sesión")
    actividad = models.TextField("actividades de la sesión", blank=True, null=True)
    comentarios = models.TextField("comentarios", blank=True, null=True)

    def __str__(self):
        return "Sesión de {} el {}".format(self.paciente, self.creado_el)

    class Meta:
        verbose_name = "sesión"
        verbose_name_plural = "sesiones"
