# conding=utf-8
from consultorio.models import Consultorio


def branding(request):
    consultorio = Consultorio.get_current()
    return {
        'PLAN_KINES': consultorio.plan,
        'NOMBRE_CONSULTORIO': consultorio.nombre,
    }
