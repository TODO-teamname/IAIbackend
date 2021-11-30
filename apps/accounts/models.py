import jwt

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from commons.models import TimeStampMixin

class UserManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        
        return user

class User(AbstractUser, TimeStampMixin):
    username = None
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email' # unique identifier of user is email
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
