from django.db import models
from django.db.models import Case, CharField, F, Value as V, When
from django.db.models.functions import Concat


class TurnoQuerySet(models.QuerySet):

    def to_export(self):
        """
        Utilizar este método para exportar el queryset a excel usando django-excel.

        """
        return self.annotate(
            Profesional=Concat('profesional__persona__nombre', V(' '),
                               'profesional__persona__apellido'),
            Cobertura=F('cobertura__nombre'),
            Paciente=Case(
                When(paciente__isnull=False, then=Concat('paciente__persona__nombre', V(' '),
                                                         'paciente__persona__apellido')),
                default=F('nombre_paciente'),
                output_field=CharField()
            ),
            NoAsistio=Case(When(no_asistio=True, then=V('Si')), default=V('No'), output_field=CharField()),
            NoAviso=Case(When(no_aviso=True, then=V('Si')), default=V('No'), output_field=CharField())
        )
