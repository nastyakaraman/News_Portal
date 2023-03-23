import os
from celery import Celery
from celery.schedules import crontab
import news
# news.tasks import send_weeklynews

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'News_Portal.settings')

app = Celery('News_Portal')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.timezone = 'Europe/London'
app.conf.enable_utc = True

app.conf.beat_schedule = {
    'action_every_30_seconds': {
        'task': 'news.tasks.send_weeklynews',
        'schedule': crontab(minute=0, hour=5,
                            day_of_week='monday'),
    },
}

