from .base import *  # noqa

INSTALLED_APPS += (
    'gunicorn',
    'raven.contrib.django.raven_compat',
)

