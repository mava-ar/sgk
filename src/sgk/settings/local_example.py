from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'b%g$gx6ovsx=dzc-7d!8i6m-d2*%g*^-^un7@l(x&)#z&c&d46'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

INSTALLED_APPS += (
    'django_extensions',
    'debug_toolbar',
)

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': "docker",
        'USER': "docker",
        'PASSWORD': "docker",
        "HOST": "127.0.0.1",
        "POST": "5432"
    }
}

COMPRESS_ENABLED = True

MIDDLEWARE_CLASSES += [
    'debug_toolbar.middleware.DebugToolbarMiddleware'
]