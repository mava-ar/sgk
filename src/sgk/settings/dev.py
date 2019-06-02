from .base import *


EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

INSTALLED_APPS += [
    'django_extensions',
    'debug_toolbar',
    'template_repl',
]

DEBUG_TOOLBAR_CONFIG = {
    'JQUERY_URL': 'http://127.0.0.1:8000/static/jquery/dist/jquery.js',
}

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware'
]

