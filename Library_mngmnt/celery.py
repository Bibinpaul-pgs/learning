from __future__ import absolute_import, unicode_literals

import os

from pytz import timezone

from celery import Celery

from django.conf import settings

from celery.schedules import crontab


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Library_mngmnt.settings")

app = Celery("Library_mngmnt")

app.conf.enable_utc = False

app.conf.update(timezone = 'Asia/Kolkata')

app.config_from_object("django.conf:settings", namespace="CELERY")


# celery beat settings

app.autodiscover_tasks(lambda:settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    'send-every-5-minutes' : {
    'task' : 'send_reminder',
    'schedule' : crontab(minute='*/5')
    }
}

@app.task(bind = True)
def debug_task(self):
    print(f'Request:{self.request!r}')