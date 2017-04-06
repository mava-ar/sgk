import factory
from datetime import date, timedelta

from django.contrib.auth.models import User

from core.models import Contacto, Profesional, Persona


class UserFactory(factory.django.DjangoModelFactory):
    first_name = factory.Faker('first_name', locale='es')
    last_name = factory.Faker('last_name', locale='es')
    email = factory.LazyAttribute(lambda o: '%s.%s@example.org' % (o.first_name.lower(), o.last_name.lower()))
    # username = factory.LazyAttribute(lambda o: '%s_%s' % (o.first_name.lower(), o.last_name.lower()))
    username = factory.Faker("user_name", locale='es')
    password = factory.PostGenerationMethodCall('set_password', 'password')

    class Meta:
        model = User


class ContactoFactory(factory.django.DjangoModelFactory):
    nombre = factory.Faker('first_name', locale='es')
    apellido = factory.Faker('last_name', locale='es')

    class Meta:
        model = Contacto


class PersonaFactory(factory.django.DjangoModelFactory):
    nombre = factory.Faker('first_name', locale='es')
    apellido = factory.Faker('last_name', locale='es')
    fecha_nacimiento = factory.Sequence(lambda n: date(2000, 1, 1) + timedelta(days=n))

    class Meta:
        model = Persona


class ProfesionalFactory(factory.django.DjangoModelFactory):
    persona = factory.SubFactory(PersonaFactory)
    usuario = factory.SubFactory(UserFactory)

    class Meta:
        model = Profesional
