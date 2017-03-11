from .dev import *
import environ


DEBUG_PROPAGATE_EXCEPTIONS = env.bool('DEBUG', True)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'sgk.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
CELERY_ALWAYS_EAGER = True
BROKER_BACKEND = 'memory'

MEDIA_ROOT = environ.Path(SITE_ROOT, '../../test_media').root

PRIVATE_STORAGE_CONTAINER = None

