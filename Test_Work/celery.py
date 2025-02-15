from __future__ import absolute_import
import os
from celery import Celery
from . import settings
from celery import current_app

current_app.conf.task_always_eager = True
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Test_Work.settings')
app = Celery('Test_Work', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

app.conf.update(
    timezone='Asia/Manila',
    enable_utc=True,
)

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(['mailer'])

