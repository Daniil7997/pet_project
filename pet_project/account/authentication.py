from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password


class EmailAuthBackend(BaseBackend):

    USER_MODEL = get_user_model()

    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = self.USER_MODEL.objects.get(email=email)
        except (self.USER_MODEL.DoesNotExist, self.USER_MODEL.MultipleObjectsReturned):
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            return None
        else:
            if (check_password(password, user.password)
                    and self.user_can_authenticate(user)):
                return user

    def get_user(self, user_id):
        try:
            user = self.USER_MODEL.objects.get(pk=user_id)
        except self.USER_MODEL.DoesNotExist:
            return None
        return user if self.user_can_authenticate(user) else None

    @staticmethod
    def user_can_authenticate(user):
        """
        Reject users with is_active=False. Custom user models that don't have
        that attribute are allowed.
        """
        return getattr(user, "is_active", False)
