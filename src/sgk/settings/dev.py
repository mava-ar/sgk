from .base import *

INSTALLED_APPS += [
    'django_extensions',
    'debug_toolbar',
    'template_repl',
]

DEBUG_TOOLBAR_CONFIG = {
    'JQUERY_URL': 'http://127.0.0.1:8000/static/jquery/dist/jquery.js',
}

MIDDLEWARE_CLASSES += [
    'debug_toolbar.middleware.DebugToolbarMiddleware'
]

