from celery.schedules import crontab
from celery.task import periodic_task
from celery.utils.log import get_task_logger
from django.conf import settings
from django.utils import timezone

from pacientes.models import Paciente
from turnos.models import Turno
from .smsc import SmscApi

logger = get_task_logger(__name__)


@periodic_task(run_every=(crontab(minute='30', hour='08')), name="send_sms_notifications", ignore_result=True)
def send_sms_notifications():
    hoy = timezone.now()
    sms_api = SmscApi()
    for turno in Turno.objects.filter(dia=hoy, paciente__isnull=False).all():
        if Paciente.objects.filter(pk=turno.paciente_id, persona__info_contacto__celular__isnull=False,
                                   persona__info_contacto__notificar_sms=True).exists():
            sms_api.send_sms(turno.paciente.persona.info_contacto.celular,
                             "Recuerde que su turno con {}, es hoy a las {} hs. {}".format(
                                 turno.profesional, turno.hora, settings.NOMBRE_CONSULTORIO))
