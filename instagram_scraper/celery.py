from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'instagram_scraper.settings')

app = Celery('instagram_scraper')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.update(
    broker_url='redis://localhost:6379/0',
    result_backend='redis://localhost:6379/0',
)

app.conf.beat_schedule = {
    'fetching_data_periodically': {
        'task': 'ig_scraper.tasks.fetch_all_influencers_data',
        'schedule': crontab(minute=0),
    },
}
