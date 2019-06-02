from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum
from django.utils.safestring import mark_safe

from core.models import Profesional
from pacientes.models import Paciente, EntradaHistoriaClinica
from dj_utils.models import BaseModel
from dj_utils.mixins import ShowInfoMixin


class MotivoConsulta(BaseModel, ShowInfoMixin):
    """
    Contiene información sobre el motivo por el cual
    el paciente debe tomar algunas sesiones.

    """
    paciente = models.ForeignKey(Paciente, verbose_name='paciente',
                                 related_name='motivos_de_consulta',
                                 on_delete=models.CASCADE)
    motivo_consulta_paciente = models.TextField(
        'motivo según el paciente', blank=True, default="",
        help_text="Signos y síntomas explicados por el paciente.")
    diagnostico_medico = models.TextField(
        'diagnóstico médico', help_text='Diagnóstico que elaboró el médico especialista.')
    evaluacion_kinesica = models.TextField(
        'evaluación kinésica', help_text='Evaluación elaborada por el kinesiólogo/a.')
    tratamientos_previos = models.TextField(
        'tratamientos previos', blank=True,
        help_text='Descripción de tratamientos previos por el mismo motivo de consulta')
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
        verbose_name = "motivo de consulta"
        verbose_name_plural = "motivos de consulta"

    def _sesiones(self, planificaciones=None):
        if not planificaciones:
            planificaciones = self.planificaciones.all()
        return Sesion.objects.filter(planificacion__in=planificaciones, fin_el__isnull=False)

    @property
    def historial_sesiones(self):
        return self._sesiones().order_by("-comienzo_el")

    @property
    def sesiones_realizadas(self):
        return self.historial_sesiones.count()

    @property
    def sesiones_planificadas(self):
        return self.planificaciones.aggregate(suma=Sum('cantidad_sesiones'))["suma"]

    @property
    def sesiones_restantes(self):
        plan = self.planificacion_actual
        if plan and plan.cantidad_sesiones:
            return plan.cantidad_sesiones - self._sesiones(planificaciones=[plan]).count()
        return 0

    @property
    def planificacion_actual(self):
        try:
            return self.planificaciones.filter(estado__in=Planificacion.estados_activos()).get()
        except:
            return None

    def sesiones_realizadas_al(self, fecha):
        return self._sesiones().filter(fin_el__lt=fecha).count()

    def planificacion_del(self, fecha):
        return self.planificaciones.filter(creado_el__lte=fecha).latest('creado_el')


class Objetivo(BaseModel, ShowInfoMixin):
    """
    Representa un objetivo del tratamiento.
    Puede haber varios para un tratamiento, y se van cumpliendo
    con el paso de las sesiones.

    """
    motivo_consulta = models.ForeignKey(
        MotivoConsulta, verbose_name='motivo de consulta', related_name='objetivos',
        on_delete=models.CASCADE)
    descripcion = models.CharField('descripción', max_length=255)
    fecha_inicio = models.DateField('fecha de inicio', null=True, auto_now_add=True)
    fecha_cumplido = models.DateField('fecha de éxito', null=True)
    observaciones = models.TextField('observaciones', blank=True)

    field_info = ('descripcion', 'observaciones', )

    def __unicode__(self):
        return u"{}".format(self.descripcion)

    class Meta:
        ordering = ('fecha_inicio', )
        verbose_name = "objectivo"
        verbose_name_plural = "objetivos"

    @property
    def cumplido(self):
        return self.fecha_cumplido is not None

    field_info = ('descripcion', 'fecha_inicio',
                  'fecha_cumplido', 'observaciones')


class Planificacion(BaseModel, ShowInfoMixin):
    """
    La planificación puede ser diseñada por el profesional, o por el médico especialista
    que indicó sesiones de kinesiología. Contiene la información sobre el tratamiento pensado
    el motivo de consulta relacionado.
    """
    PLANIFICADO = 1
    EN_CURSO = 2
    FINALIZADO = 3
    CANCELADO = 4

    PLANIFICACION_ESTADO = (
        (PLANIFICADO, 'Planificado'),
        (EN_CURSO, 'En curso'),
        (FINALIZADO, 'Finalizado'),
        (CANCELADO, 'Cancelado')
    )
    motivo_consulta = models.ForeignKey(MotivoConsulta, related_name='planificaciones', on_delete=models.CASCADE)
    fecha_ingreso = models.DateField(
        'fecha de ingreso', null=True,
        help_text="Fecha de inicio de tratamiento, normalmente la fecha de la primer sesión.")
    fecha_alta = models.DateField(
        'fecha de alta', null=True, blank=True, help_text='fecha de alta tentativa.')
    por_sesion = models.BooleanField(
        'por sesión', default=False,
        help_text=('Seleccione esta opción si el tratamiento '
                   'no depende de una cantidad determinada de sesiones.'))
    cantidad_sesiones = models.IntegerField(
        'cantidad de sesiones', null=True, blank=True,
        help_text='Cantidad de sesiones necesarias recetadas por el médico.')
    frecuencia = models.PositiveIntegerField(
        'frecuencia semanal', default=1, validators=[MinValueValidator(1), MaxValueValidator(7)])
    estado = models.IntegerField("estado", choices=PLANIFICACION_ESTADO, default=1)
    comentarios = models.TextField("comentarios", blank=True, null=True)
    conclusion = models.TextField("conclusión", blank=True, null=True)

    motivo_finalizacion = models.TextField("motivo de finalización", blank=True, null=True)

    def __str__(self):
        return "Planificación de {} - {} sesiones - {}".format(
            self.motivo_consulta.paciente, self.cantidad_sesiones, self.estado
        )

    field_info = ('fecha_ingreso', 'fecha_alta',
                  'por_sesion', 'cantidad_sesiones',
                  'frecuencia', 'estado', 'comentarios', 'conclusion')

    class Meta:
        verbose_name_plural = 'planificaciones'
        verbose_name = 'planificación'

    def clean(self):
        if self.por_sesion and self.cantidad_sesiones:
            raise ValidationError("Debe seleccionar la opción 'Por sesión' o especificar 'Cantidad de sesiones', no ambos.")
        elif not any([self.por_sesion, self.cantidad_sesiones is not None and self.cantidad_sesiones > 0]):
            raise ValidationError("Debe seleccionar la opción 'Por sesión' o especificar 'Cantidad de sesiones'.")

    @classmethod
    def estados_activos(self):
        return [self.PLANIFICADO, self.EN_CURSO, ]


class Sesion(BaseModel, ShowInfoMixin):
    """
    Representa una sesión tomada por el paciente. En ella, se indica
    como se encuentra el paciente previamente, que actividades se realizan,
    y la duración.
    """
    paciente = models.ForeignKey(Paciente, related_name='sesiones_paciente', on_delete=models.CASCADE)
    profesional = models.ForeignKey(Profesional, related_name="sesiones", on_delete=models.CASCADE)
    planificacion = models.ForeignKey(Planificacion, related_name='sesiones', null=True, on_delete=models.SET_NULL)
    fecha = models.DateField("fecha")
    duracion = models.PositiveSmallIntegerField("duración de la sesión", default=60,
                                                help_text="Duración de la sesión en minutos")
    estado_paciente = models.TextField(
        "estado de paciente", blank=True, null=True,
        help_text="Descripción de cómo se siente el paciente antes de la sesión")
    actividad = models.TextField("actividades de la sesión", blank=True, null=True)
    comentarios = models.TextField("comentarios", blank=True, null=True)
    comienzo_el = models.DateTimeField("fecha y hora de comienzo de sesión", auto_now_add=True)
    fin_el = models.DateTimeField("fecha y hora de fin de sesión", null=True)

    def __str__(self):
        return "Sesión de {} el {}".format(self.paciente, self.creado_el)

    class Meta:
        verbose_name = "sesión"
        verbose_name_plural = "sesiones"

    @property
    def long_description(self):
        txt = ''
        if self.estado_paciente:
            txt += "<strong>Estado del paciente:</strong> {}".format(self.estado_paciente)
        if self.actividad:
            txt += "&nbsp;&nbsp;<strong>Actividad:</strong> {}".format(self.actividad)
        if self.comentarios:
            txt += "&nbsp;&nbsp;<strong>Comentarios:</strong> {}".format(self.comentarios)
        if not txt:
            txt = 'Sin comentarios.'
        return mark_safe(txt)

    field_info = ('fecha', 'duracion', 'estado_paciente', 'actividad',
                  'comentarios')
