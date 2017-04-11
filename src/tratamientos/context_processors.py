from core.models import Profesional
from tratamientos.models import Sesion


def sesiones_activas(request):
    if request.user.is_authenticated():
        try:
            sesiones = Sesion.objects.filter(
                profesional=request.user.profesional,
                fin_el__isnull=True).select_related('planificacion__motivo_consulta', 'paciente__persona')
            data = []
            for sesion in sesiones:
                data.append({
                    'paciente_nombre': str(sesion.paciente.persona),
                    'comienzo_el': sesion.comienzo_el,
                    'duracion': sesion.duracion,
                    'persona': sesion.paciente.persona,
                    'paciente_pk': sesion.paciente_id,
                    'motivo_pk': sesion.planificacion.motivo_consulta_id
                })
            return {'sesiones_activas': data}
        except Profesional.DoesNotExist:
            pass
    return {}
