from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
broker_connection_retry_on_startup = True

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'match_online.settings')

app = Celery('match_online', broker='redis://127.0.0.1:6379/0')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
