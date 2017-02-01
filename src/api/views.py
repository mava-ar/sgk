from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from turnos.models import Turno

from core.models import Profesional
from .serializers import TurnoCalendarSerializer


class AuthView(APIView):
    permission_classes = (IsAuthenticated,)


class TurnoCalendarSet(viewsets.ModelViewSet, AuthView):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Turno.objects.all()
    serializer_class = TurnoCalendarSerializer
    http_method_names = ['get', 'put', ]

    def get_queryset(self):

        qs = super(TurnoCalendarSet, self).get_queryset()
        # si el usuario tiene un profesional asociado, sólo mostrar sus turnos
        try:
            qs = qs.filter(profesional=self.request.user.profesional)
        except Profesional.DoesNotExist:
            pass
        start = self.request.GET.get("start", "")
        end = self.request.GET.get("end", "")
        if start:
            qs = qs.filter(dia__gte=start)
        if end:
            qs = qs.filter(dia__lte=end)
        return qs
