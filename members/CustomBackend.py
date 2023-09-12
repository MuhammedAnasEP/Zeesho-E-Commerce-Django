from django.contrib.auth.backends import BaseBackend
from .models import CustomUser
from django.contrib.auth import get_user_model
from django.contrib.auth.models import auth

User = get_user_model()

class CustomBackend(BaseBackend):

    def authenticate(request, phone_number):
    # Check the token and return a user.
        try:
            phone_number=phone_number[3:]
            print(phone_number)
            user = User.objects.get(phone_number=phone_number)
            auth.login(request,user,backend='django.contrib.auth.backends.ModelBackend')
        except User.DoesNotExist:
            return None