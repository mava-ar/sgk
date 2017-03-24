# conding=utf-8
from django.conf import settings


def branding(request):
    return {
        'PLAN_KINES': settings.PLAN_KINES,
        'NOMBRE_CONSULTORIO': settings.NOMBRE_CONSULTORIO,
    }
