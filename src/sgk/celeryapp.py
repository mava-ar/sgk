from __future__ import absolute_import

import os
from tenant_schemas_celery.app import CeleryApp
from django.conf import settings
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
if os.path.isfile(os.path.join(os.path.abspath('.'), 'sgk', 'settings', 'local.py')):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sgk.settings.local')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sgk.settings.production')

app = CeleryApp('sgk')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


# schedule for all environment
app.conf.beat_schedule = {
    # 'send_sms_notifications': {
    #     'task': 'send_sms_notifications',
    #     'schedule': crontab(minute='0', hour='08')  # Execute every day at 8:00 am
    # },
}
