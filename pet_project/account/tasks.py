import datetime

from django.contrib.auth.hashers import make_password
from django.db import transaction
from celery import shared_task

from account.models import UserAuth, Profile


# -------------------------- CELERY ----------------------------------
# эта задача создавалась для тестирования CELERY
@shared_task
@transaction.atomic
def task_registration_db_insert(data):
    data['password'] = make_password(data['password'])
    user = UserAuth.objects.create(
        password=data['password'],
        email=data['email']
    )
    user_profile = Profile.objects.create(
        name=data['name'],
        birthday=data['birthday'],
        sex=data['sex'],
        i_search=data['i_search'],
        auth_id=user.id,
    )
    return user_profile


# ------------------------ CELERY-BEAT ------------------------------
# периодическая задача Celery для удаления не подтвержденных пользователей
@shared_task
def deleting_inactive_accounts():
    delete_time = datetime.datetime.now() - datetime.timedelta(minutes=60)
    UserAuth.objects.filter(is_active=False, created_at__lt=delete_time).delete()
