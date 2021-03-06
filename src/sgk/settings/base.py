# -*- coding: utf-8 -*-
"""
Django settings for kines project.

Generated by 'django-admin startproject' using Django 1.8.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""
from sys import path
from datetime import timedelta
import environ
root = environ.Path(__file__) - 3  # three folder back (/src/sgk/settings/ - 3 = src/)

# PATH CONFIGURATION
# Absolute filesystem path to the top-level project folder:
SITE_ROOT = root()

# Absolute filesystem path to the Django project directory:
DJANGO_ROOT = root.path("sgk/").root

# Add our project to our pythonpath, this way we don't need to type our project
# name in our dotted import paths:
path.append(DJANGO_ROOT)
# END PATH CONFIGURATION

env = environ.Env(
    SECRET_KEY=str,
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, ['127.0.0.1:8000']),
    DATABASE_URL=str,
)

environ.Env.read_env(root.path('.env').root)  # reading .env file

DEBUG = env.bool('DEBUG', False)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['127.0.0.1:8000'])
SECRET_KEY = env.str('SECRET_KEY', '1234568901234567890')
SITE_ID = 1
ADMINS = [
    (env.str("ADMIN_NAME", 'Matias Varela'),
     env.str("ADMIN_EMAIL", 'matu.varela@gmail.com'))
]

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/login/'
LOGOUT_URL = '/'

# Application definition
SHARED_APPS = [
    'django_tenants',  # mandatory
    'consultorio',

    'django.contrib.contenttypes',

    # everything below here is optional
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
]

TENANT_APPS = [
    'material',
    # 'material.frontend',
    # 'material.admin',

    # The following Django contrib apps must be in TENANT_APPS
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',

    'djangobower',
    'pipeline',
    'bootstrap3',
    'easy_thumbnails',
    'datetimewidget',
    'djangoformsetjs',
    'corsheaders',
    'django_tables2',
    'django_filters',
    'crispy_forms',
    'rest_framework',

    # own
    'frontend',
    'dj_utils',
    'dj_auth',
    'core',
    'coberturas_medicas',
    'pacientes',
    'tratamientos',
    'turnos',
    'notifications',
]

INSTALLED_APPS = list(SHARED_APPS) + [app for app in TENANT_APPS if app not in SHARED_APPS]

MIDDLEWARE = [
    'django_tenants.middleware.main.TenantMainMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'pipeline.middleware.MinifyHTMLMiddleware'
]

ROOT_URLCONF = 'sgk.urls'
PUBLIC_SCHEMA_URLCONF = 'sgk.urls_public'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.template.context_processors.debug',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "tratamientos.context_processors.sesiones_activas",
                "frontend.context_processors.branding"
            ],
        },
    },
]

WSGI_APPLICATION = 'sgk.wsgi.application'

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    )
}
JWT_EXPIRATION_DELTA = timedelta(minutes=60)
JWT_ALLOW_REFRESH = True

CRISPY_TEMPLATE_PACK = 'bootstrap3'
# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases


TENANT_MODEL = "consultorio.Consultorio" #  app.Model
TENANT_DOMAIN_MODEL = "consultorio.Dominio"  # app.Model

DATABASES = {
    'default': env.db(),
}

DATABASES["default"].update({
    'ENGINE': 'django_tenants.postgresql_backend'
})

DATABASE_ROUTERS = (
    'django_tenants.routers.TenantSyncRouter',
)

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'es'

LANGUAGES = [
    ('es', 'Español'),
]

TIME_ZONE = 'America/Argentina/Mendoza'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = (root.path("sgk/locale/").root, )

DATE_INPUT_FORMATS = ['%d/%m/%Y', ]
DATE_FORMAT = 'd/m/Y'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'djangobower.finders.BowerFinder',
    'pipeline.finders.PipelineFinder',
)

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'
MEDIA_ROOT = root.path(env.str('MEDIA_ROOT', '../media')).root
STATIC_ROOT = root.path(env.str('STATIC_ROOT', '../collected_static')).root

BOWER_ROOT = root.path('../components')
PIPELINE_SASS_ARGUMENTS = "-p 8 -I '%s' -I '%s'" % (
    BOWER_ROOT.path('bower_components/bootstrap-sass/assets/stylesheets/').root,
    BOWER_ROOT.path('bower_components/bootstrap-sass/assets/fonts/').root
)

PIPELINE = {
    'PIPELINE_ENABLED': env.bool('PIPELINE_ENABLED', True),
    'STORAGE': STATICFILES_STORAGE,
    'STYLESHEETS': {
        'base': {
            'source_filenames': (
                'font-awesome/css/font-awesome.min.css',
                'bootstrap/dist/css/bootstrap.css',
                'bootstrap-material-design/dist/css/bootstrap-material-design.css',
                'bootstrap-material-design/dist/css/ripples.css',
                'chosen/chosen.min.css',
                'animate.css/animate.min.css',
                'css/base.scss',
            ),
            'output_filename': 'css/base.css',
            'extra_context': {
                'media': 'screen,projection',
            },
        },
        'fullcalendar': {
            'source_filenames': (
                'fullcalendar/dist/fullcalendar.css',
            ),
            'output_filename': 'css/fullcalendar.css',
            'extra_content': {
                'media': 'screen,projection',
            }
        }
    },
    'JAVASCRIPT': {
        'head_js': {
            'source_filenames': (
                'js/vendor/modernizr-2.8.3.min.js',
                'jquery/dist/jquery.js',
            ),
            'output_filename': 'js/head.js'
        },
        'base_js': {
            'source_filenames': (
                'bootstrap/dist/js/bootstrap.js',
                'bootstrap3-dialog/dist/js/bootstrap-dialog.js',
                'bootstrap-material-design/dist/js/material.js',
                'bootstrap-material-design/dist/js/ripples.js',
                'js/kines.js',
            ),
            'output_filename': 'js/base.js',
        },
        'plugins_js': {
            'source_filenames': (
                'chosen/chosen.jquery.min.js',
                'PACE/pace.js',
                'jquery-sticky/jquery.sticky.js',
                'jquery-form/jquery.form.js',
                'jquery.are-you-sure/jquery.are-you-sure.js',
            ),
            'output_filename': 'js/plugins.js'
        },
        'fullcalendar_js': {
            'source_filenames': (
                'moment/moment.js',
                'fullcalendar/dist/fullcalendar.js',
                'fullcalendar/dist/lang/es.js',
            ),
            'output_filename': 'js/fullcalendar.js',
        },
        'letterjs': {
            'source_filenames': (
                'js/animations/segment.min.js',
                'js/animations/d3-ease.v0.6.js',
                'letteringjs/jquery.lettering.js',
                'js/animations/letters.js',
                'mojs/build/mo.min.js',
                'typed.js/js/typed.js',
            ),
            'output_filename': 'js/letters.js'
        }
    },
    'COMPILERS': (
        'pipeline.compilers.sass.SASSCompiler',
    ),
    'SASS_BINARY': 'sassc',
    'CSS_COMPRESSOR': None,
    'JS_COMPRESSOR': None,
    # 'SASS_ARGUMENTS': PIPELINE_SASS_ARGUMENTS,
    'DISABLE_WRAPPER': True
}


BOWER_INSTALLED_APPS = (
    'jquery#2.1.4',
    'bootstrap#3.3.7',
    'fontawesome#4.3.0',
    'bootstrap3-dialog#1.34.9',
    'chosen#1.4.2',
    'bootstrap-datepicker#1.6.1',
    'pace#1.0.2',
    'jquery-sticky#^1.0.3',
    'jquery.countdown#2.1.0',
    'jquery-form#3.46.0',
    'fullcalendar#2.9.1',
    'jquery.are-you-sure#^1.9.0',
    'bootstrap-material-design#0.5.9',
    'animate.css#^3.5.2',
    # duda
    'd3-ease',
    'letteringjs',
    'mojs',
    'typed.js'
)

THUMBNAIL_ALIASES = {
    '': {
        'avatar': {'size': (50, 50), 'crop': True},
        'perfil': {'size': (250, 250), 'crop': True},
    },
}


# Default settings
BOOTSTRAP3 = {
    # Label class to use in horizontal forms
    'horizontal_label_class': 'col-sm-2',
    # Field class to use in horizontal forms
    'horizontal_field_class': 'col-sm-10',
    'set_placeholder': False,
}

CORS_ORIGIN_ALLOW_ALL = True

EMAIL_CONFIG = env.email_url(
    'EMAIL_URL', default='smtp://user@:password@localhost:25')

vars().update(EMAIL_CONFIG)

# CELERY SETTINGS
BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

# sentry
RAVEN_CONFIG = {
    'dsn': env.str('SENTRY_URL', ''),
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    # 'release': raven.fetch_git_sha(os.path.dirname(__file__)),
}

DJAUTH_BASE_TEMPLATE = 'base.html'

# smsc service
SMSC_ALIAS = env.str('SMSC_ALIAS', '')
SMSC_APIKEY = env.str('SMSC_APIKEY', '')
