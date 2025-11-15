from django.contrib.auth.hashers import make_password
from django.db import transaction

from account.models import UserAuth, Profile


@transaction.atomic
def registration_db_insert(data):
    print(data, 'DATA UTILS.py')
    data['password'] = make_password(data['password'])
    user = UserAuth.objects.create(
        password=data['password'],
        email=data['auth']['email']
    )
    user_profile = Profile.objects.create(
        name=data['name'],
        birthday=data['birthday'],
        sex=data['sex'],
        i_search=data['i_search'],
        auth_id=user.id,
    )
    return user_profile
