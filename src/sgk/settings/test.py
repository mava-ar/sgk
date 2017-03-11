from .dev import *

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

MEDIA_ROOT = normpath(join(SITE_ROOT, '../../test_media'))

PRIVATE_STORAGE_CONTAINER = None

