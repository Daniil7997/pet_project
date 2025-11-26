import os

from celery import Celery


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pet_project.settings')
app = Celery('pet_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Настройки расписания для Celery Beat
app.conf.beat_schedule = {
    'delete-unverified-users-every-hour': {
        'task': 'account.tasks.deleting_inactive_accounts',
        'schedule': 1800.0,  # Каждые 1800 секунд (30 минут)
        # Или:
        # 'schedule': crontab(minute=0, hour='*/1'),  # Каждый час в 0 минут
    },
}


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
