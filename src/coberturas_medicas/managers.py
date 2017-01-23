from django.db import models


class CoberturaManager(models.Manager):
    """
    La cobertura particular la debemos considerar fuera del grupo de coberturas.
    """

    def get_base_queryset(self):
        return super(CoberturaManager, self).get_queryset()

    def get_queryset(self):
        return super(CoberturaManager, self).get_queryset().filter(cobertura_propia=False)

    def get_particular(self):
        return self.get_base_queryset().get(cobertura_propia=True)
