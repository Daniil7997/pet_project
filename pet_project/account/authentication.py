from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password, make_password

from .models import UserList


class EmailAuthBackend(BaseBackend):

    def authenticate(self, request, email=None, password=None, **kwargs):
        user_model = UserList
        try:
            user = user_model.objects.get(email=email)
            print(f'{check_password(password, user.password)} - CHECK_PASSWORD')
        except (user_model.DoesNotExist, user_model.MultipleObjectsReturned):
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            return None
        else:
            if (check_password(password, user.password)
                    and self.user_can_authenticate(user)):
                return user
    #
    # def get_user(self, user_id):
    #     print('вызван get_user')
    #     try:
    #         user = UserList.objects.get(pk=user_id)
    #         print(f'{user} - user \n{user_id} - user_id')
    #     except UserList.DoesNotExist:
    #         return None
    #     return user if self.user_can_authenticate(user) else None

    @staticmethod
    def user_can_authenticate(user):
        """
        Reject users with is_active=False. Custom user models that don't have
        that attribute are allowed.
        """
        return getattr(user, "is_active", True)
