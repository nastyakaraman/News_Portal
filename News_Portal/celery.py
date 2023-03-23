import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'News_Portal.settings')

app = Celery('News_Portal')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

'''app.conf.beat_schedule = {
    'action_every_30_seconds': {
        'task': 'tasks.action',
        'schedule': crontab(minute=0, hour=8,
                            day_of_week='monday')
        'args': (args),
    },
}'''

