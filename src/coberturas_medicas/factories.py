import factory

from coberturas_medicas.models import Cobertura


class CoberturaFactory(factory.django.DjangoModelFactory):
    nombre = factory.Sequence(lambda n: 'prepaga %s' % n)

    class Meta:
        model = Cobertura
