from django.utils import timezone

from celery.utils.log import get_task_logger

from consultorio.models import Consultorio
from pacientes.models import Paciente
from turnos.models import Turno
from sgk.celeryapp import app
from .smsc import SmscApi

logger = get_task_logger(__name__)


@app.task(name="send_sms_notifications")
def send_sms_notifications():
    consultorio = Consultorio.get_current()
    hoy = timezone.now()
    sms_api = SmscApi()
    for turno in Turno.objects.filter(dia=hoy, paciente__isnull=False).all():
        if Paciente.objects.filter(pk=turno.paciente_id, persona__info_contacto__celular__isnull=False,
                                persona__info_contacto__notificar_sms=True).exists():
            sms_api.send_sms(turno.paciente.persona.info_contacto.celular,
                            "Recuerde que su turno con {}, es hoy a las {} hs. {}".format(
                                turno.profesional, turno.hora, consultorio.nombre))
