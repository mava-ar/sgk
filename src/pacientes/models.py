from django.db import models

from model_utils.managers import InheritanceManager

from coberturas_medicas.models import Cobertura
from core.models import Persona, Profesional
from dj_utils.mixins import ShowInfoMixin
from dj_utils.models import BaseModel


class Paciente(BaseModel):
    """
    Persona que se atiende en el lugar.
    """
    persona = models.OneToOneField(Persona, verbose_name='persona')

    fecha_ingreso = models.DateField('fecha de ingreso')
    observaciones = models.TextField('observaciones', blank=True)
    # relaciones
    cobertura_medica = models.ForeignKey(Cobertura, verbose_name='cobertural', null=True)

    def __str__(self):
        return "{}".format(self.persona)

    class Meta:
        verbose_name = "paciente"
        verbose_name_plural = "pacientes"

    def tratamiento_activo(self):
        from tratamientos.models import Planificacion
        try:
            return self.motivos_de_consulta.filter(planificaciones__estado__in=Planificacion.estados_activos()).get()
        except:
            return None

class RegistroBiometrico(BaseModel, ShowInfoMixin):
    """
    Registro de datos biométricos. Como avarían en el tiempo, se deja constancia de la
    fecha
    """
    paciente = models.ForeignKey(Paciente, related_name='registros_biometricos')
    peso = models.DecimalField('peso (kg)', max_digits=5, decimal_places=2, null=True)
    altura = models.DecimalField('altura (mts)', max_digits=5, decimal_places=2, null=True)
    # demás datos biomédicos.
    #
    profesional = models.ForeignKey(Profesional)
    # archivos

    def __str__(self):
        return "Registro biométrico de {} ({})".format(self.paciente, self.creado_el)

    class Meta:
        verbose_name = 'registro biométrico'
        verbose_name_plural = 'registros biométricos'

    field_info = ('modificado_el', 'peso', 'altura', )


class Antecedente(BaseModel, ShowInfoMixin):
    """
    Representa la historia médica del paciente.
    Contiene datos médicos y relevantes sobre el paciente.

    """
    paciente = models.OneToOneField(Paciente)
    patologicos = models.TextField('patológicos', blank=True)
    quirurgicos = models.TextField('quirúrgicos', blank=True)
    traumaticos = models.TextField('traumáticos', blank=True)
    alergicos = models.TextField('alérgicos', blank=True)
    heredo_familiar = models.TextField('heredo familiar', blank=True)
    habitos_fisiologicos = models.TextField('hábitos fisiológicos', blank=True)
    actividad_fisica= models.TextField('actividad física', blank=True)
    habitos_patologicos = models.TextField('hábitos patológicos', blank=True)
    medicaciones = models.TextField('medicaciones', blank=True)
    estudios_complementarios = models.TextField('estudios complementarios', blank=True)
    menarca = models.DateField('MENARCA', null=True)
    fum = models.DateField('FUM', null=True)
    tipo_partos = models.TextField('tipo de partos', blank=True)
    observaciones = models.TextField('observaciones', blank=True)

    def __unicode__(self):
        return "Antecedentes de {}".format(
                self.paciente.persona.nombre)

    class Meta:
        verbose_name = "antecedente"
        verbose_name_plural = "antecedentes"

    field_info = ('patologicos', 'quirurgicos', 'traumaticos', 'alergicos', 'heredo_familiar',
                  'habitos_fisiologicos', 'actividad_fisica', 'habitos_patologicos', 'medicaciones',
                  'estudios_complementarios', 'menarca', 'fum', 'tipo_partos', 'observaciones')



class EntradaHistoriaClinica(BaseModel, ShowInfoMixin):
    paciente = models.ForeignKey(Paciente, related_name="entradas_historiaclinica")
    profesional = models.ForeignKey(Profesional)

    objects = InheritanceManager()

    class Meta:
        verbose_name_plural = "Entradas de historia clínica"
        verbose_name = "Entrada de historia clínica"

    def __str__(self):
        return "Entrada de {} por {}".format(self.paciente, self.profesional)



class ComentariosHistoriaClinica(EntradaHistoriaClinica):
    """
    Representa una entrada en la historia clínica del paciente.
    """
    comentarios = models.TextField(verbose_name="comentarios")

    class Meta:
        verbose_name_plural = "comentarios de historia clinica"
        verbose_name = "comentario de historia clinica"

    def __str__(self):
        return "Comentario de {}".format(self.paciente)

    field_info = ('comentarios', )


class ImagenesHistoriaClinica(EntradaHistoriaClinica):
    """
    Representa una imagen ingresada en la historia clinica
    """
    imagen = models.ImageField(verbose_name="imágen", upload_to="historia_imagenes")
    comentarios = models.TextField(verbose_name="comentarios" ,null=True, blank=True)

    class Meta:
        verbose_name_plural = "imágenes de historia clínica"
        verbose_name = "imagen de historia clínica"

    def __str__(self):
        return "Imágen de {}".format(self.paciente)

    field_info = ('imagen', 'comentarios', )