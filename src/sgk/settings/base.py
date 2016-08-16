"""
Django settings for zillepro_web project.

Generated by 'django-admin startproject' using Django 1.8.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

from os.path import abspath, basename, dirname, join, normpath
from sys import path

########## PATH CONFIGURATION
# Absolute filesystem path to the Django project directory:
DJANGO_ROOT = dirname(dirname(abspath(__file__)))

# Absolute filesystem path to the top-level project folder:
SITE_ROOT = dirname(DJANGO_ROOT)

# Site name:
SITE_NAME = basename(DJANGO_ROOT)

# Add our project to our pythonpath, this way we don't need to type our project
# name in our dotted import paths:
path.append(DJANGO_ROOT)
########## END PATH CONFIGURATION

ALLOWED_HOSTS = []
SITE_ID = 1

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/login/'
LOGOUT_URL = '/'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'djangobower',
    'pipeline',
    'bootstrap3',
    'compressor',
    'easy_thumbnails',
    'datetimewidget',
    'djangoformsetjs',

    'frontend',
    'dj_utils',
    'dj_auth',
    'core',
    'coberturas_medicas',
    'pacientes',
    'tratamientos',
    'turnos',
    'rest_framework',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'sgk.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                "django.template.context_processors.media",
                "django.template.context_processors.static",
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
    ]
}

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join(DJANGO_ROOT, 'db.sqlite3'),
    }
}


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

LANGUAGE_CODE = 'es-ar'

TIME_ZONE = 'America/Argentina/Mendoza'

USE_I18N = False

USE_L10N = False

USE_TZ = True

# LOCALE_PATHS = (normpath(join(DJANGO_ROOT, 'locale')), )

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
    'compressor.finders.CompressorFinder',
)

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'
MEDIA_ROOT = normpath(join(SITE_ROOT, '../media'))
STATIC_ROOT = normpath(join(SITE_ROOT, '../collected_static'))

BOWER_COMPONENTS_ROOT = normpath(join(SITE_ROOT, '../components'))
PIPELINE_SASS_ARGUMENTS = "-p 8 -I '%s' -I '%s'" % (
         join(BOWER_COMPONENTS_ROOT, 'bower_components/bootstrap-sass/assets/stylesheets/'),
         join(BOWER_COMPONENTS_ROOT, 'bower_components/bootstrap-sass/assets/fonts/')
)

PIPELINE = {
    'PIPELINE_ENABLED': False,
    'STORAGE': STATICFILES_STORAGE,
    'STYLESHEETS': {
        'base': {
            'source_filenames': (
                'css/normalize.css',
                'css/boilerplate_main.css'
                'font-awesome/css/font-awesome.min.css',
                'bootstrap-sass/assets/stylesheets/_bootstrap.scss',
                'bootstrap3-dialog/dist/css/bootstrap-dialog.css',
                'font-awesome/css/font-awesome.min.css',
                # 'bootstrap-datepicker/dist/css/bootstrap-datepicker3.css',
                'chosen/chosen.min.css',
                'css/pastel-stream.css',
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
                'bootstrap-sass/assets/javascripts/bootstrap.js',
                'bootstrap3-dialog/dist/js/bootstrap-dialog.js',
                'chosen/chosen.jquery.min.js',
                'js/main.js',
                'js/plugins.js',
            ),
            'output_filename': 'js/base_js.js',
        },
        'plugins_js': {
            'source_filenames': (
                # 'bootstrap-datepicker/dist/js/bootstrap-datepicker.js',
                # 'bootstrap-datepicker/dist/locales/bootstrap-datepicker.es.min.js',
                'PACE/pace.js',
                'StickyTableHeaders/js/jquery.stickytableheaders.min.js',
                'jquery-form/jquery.form.js'
            ),
            'output_filename': 'js/plugins.js',
        },
        'fullcalendar_js': {
            'source_filenames': (
                'moment/moment.js',
                'fullcalendar/dist/fullcalendar.js',
                'fullcalendar/dist/lang/es.js',
            ),
            'output_filename': 'js/fullcalendar.js',
        },
    },
    'COMPILERS': (
        'pipeline.compilers.sass.SASSCompiler',
    ),
    'SASS_BINARY': 'sassc',
    'CSS_COMPRESSOR': None,
    'JS_COMPRESSOR': None,
    'SASS_ARGUMENTS': PIPELINE_SASS_ARGUMENTS,
    'DISABLE_WRAPPER': True
}

# django-compressor settings
COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)


BOWER_INSTALLED_APPS = (
    'jquery#2.1.4',
    'bootstrap-sass#3.3.6',
    'fontawesome#4.3.0',
    'bootstrap3-dialog#1.34.9',
    'chosen#1.4.2',
    'bootstrap-datepicker#1.6.1',
    'pace#1.0.2',
    'StickyTableHeaders#0.1.19',
    # 'django-dynamic-formset',
    'jquery.countdown#2.1.0',
    'jquery-form#3.46.0',
    'fullcalendar'
)

THUMBNAIL_ALIASES = {
    '': {
        'avatar': {'size': (50, 50), 'crop': True},
        'perfil': {'size': (250, 250), 'crop': True},
    },
}


# CELERY SETTINGS
# BROKER_URL = 'redis://localhost:6379/0'
# CELERY_RESULT_BACKEND = 'redis://localhost:6379'
# CELERY_ACCEPT_CONTENT = ['application/json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'
# CELERY_TIMEZONE = TIME_ZONE

# Default settings
# BOOTSTRAP3 = {
#      # Label class to use in horizontal forms
#     'horizontal_label_class': 'col-sm-2',
#
#     # Field class to use in horizontal forms
#     'horizontal_field_class': 'col-sm-10',
# }