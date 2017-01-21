from .models import Sesion


def sesiones_activas(request):
    sesiones = Sesion.objects.filter(fin_el__isnull=True).select_related('motivo_consulta', 'paciente__persona')
    data = []
    for sesion in sesiones:
        data.append({
            'paciente_nombre': str(sesion.paciente.persona),
            'comienzo_el': sesion.comienzo_el,
            'duracion': sesion.duracion,
            'persona': sesion.paciente.persona,
            'paciente_pk': sesion.paciente_id,
            'motivo_pk': sesion.motivo_consulta_id
        })
    return {'sesiones_activas': data}
