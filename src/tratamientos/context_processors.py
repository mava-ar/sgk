from core.models import Profesional
from tratamientos.models import Sesion
from django_tenants.utils import get_tenant_model, get_public_schema_name


def sesiones_activas(request):
    tenant_model = get_tenant_model()
    if tenant_model.get_current().schema_name == get_public_schema_name():
        return {}
    if request.user.is_authenticated:
        try:
            sesiones = Sesion.objects.filter(
                profesional=request.user.profesional, planificacion__isnull=False,
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
