from django.db import models
from django.conf import settings

# Class that handles everything non-authentication related.
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #TODO

class Organization(models.Model):
    # Note: maybe implement encryption? Also not THAT important. What is more important is that the server is secure.
    token = models.CharField(max_length=100)



class Mooclet(models.Model):
    mooclet_name = models.CharField(max_length=100)
    mooclet_id = models.IntegerField(null=True)
    policy_id = models.IntegerField()
