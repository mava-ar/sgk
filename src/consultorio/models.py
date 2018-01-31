from django.db import models

from tenant_schemas.models import TenantMixin

from dj_utils.models import BaseModel


class Consultorio(TenantMixin, BaseModel):
    nombre = models.CharField(max_length=100)
    pagado_hasta =  models.DateField(null=True)
    on_trial = models.BooleanField()

    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'consultorio'
        verbose_name_plural = 'consultorios'

