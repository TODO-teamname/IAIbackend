from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# class for information about authentication. NOTE: combine with user in future, just using this for ease of programming
class User(AbstractBaseUser):
    email = models.EmailField(('email address'), unique=True)

    USERNAME_FIELD = 'email' # unique identifier of user is email
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
