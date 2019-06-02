from django.db import models

from django_tenants.models import TenantMixin, DomainMixin

from dj_utils.models import BaseModel


class Consultorio(TenantMixin, BaseModel):
    PLANES = (
        (1, 'Básico'),
        (2, 'Estándar'),
        (3, 'Premium'),
    )
    nombre = models.CharField(max_length=100)
    pagado_hasta =  models.DateField(null=True, blank=True)
    on_trial = models.BooleanField(default=True)

    plan = models.IntegerField(choices=PLANES, default=1)

    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'consultorio'
        verbose_name_plural = 'consultorios'

    @classmethod
    def get_current(cls):
        from django.db import connection
        return connection.tenant


class Dominio(DomainMixin):

    def __str__(self):
        return self.domain
