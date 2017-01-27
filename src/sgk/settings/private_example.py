# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': "",
        'USER': "",
        'PASSWORD': "",
        "HOST": "",
        "POST": "5432"
    }
}

ALLOWED_HOSTS = ['127.0.0.1', ]

# smsc service
SMSC_ALIAS = ''
SMSC_APIKEY = ''
