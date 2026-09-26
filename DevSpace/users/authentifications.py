from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailAuthBackend(ModelBackend):



    def authenticate(self, request, **kwargs):
        email = kwargs.get('username')
        password = kwargs.get('password')
        users = get_user_model()
        try:

            user = get_user_model().objects.get(email=email)

        except (users.DoesNotExist, users.MultipleObjectsReturned):

            return None


        if user.check_password(password):
            return user

        return None

