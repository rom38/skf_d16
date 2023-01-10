import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'artboard.settings')

app = Celery('news_portal')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'clear_board_every_minute': {
        'task': 'articles.tasks.news_notify_weekly_task',
        # еженедельная рассылка с последними новостями
        # (каждый понедельник в 8:00 утра).
        'schedule': crontab(day_of_week="mon", hour="08", minute="00"),
        # рассылка каждые 2 минуты
        # 'schedule': crontab(minute='*/2'),
    },
}
