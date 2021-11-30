from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from commons.models import TimeStampMixin

PERMISSION_LEVELS = (
    ("ADMIN", "admin"),
    ("STAFF", "staff")
)

# Class that handles everything non-authentication related.
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    secondary_email = models.EmailField(null=True)

# Hooks up profile so that it is created when a user is created.
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

class Organization(models.Model):
    # Note: maybe implement encryption? Also not THAT important. What is more important is that the server is secure.
    token = models.CharField(max_length=100)
    name = models.CharField(max_length=100, null=False)
    dateRegistered = models.DateField(null=False)

class Membership(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    permission = models.CharField(null=False, choices=PERMISSION_LEVELS,  max_length=5)
    dateRegistered = models.DateField(null=False)

class Study(models.Model):
    name = models.CharField(max_length=100)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    dateRegistered = models.DateField(null=False)

class Mooclet(models.Model):
    study = models.ForeignKey(Study, on_delete=models.CASCADE)
    external_id = models.IntegerField(null=False)
