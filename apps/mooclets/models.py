from django.db import models
from commons.models import TimeStampMixin
from organizations.models import Organization

PERMISSION_LEVELS = (
    ("ADMIN", "admin"),
    ("STAFF", "staff")
)

"""
# Class that handles everything non-authentication related.
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    secondary_email = models.EmailField(null=True)

# Hooks up profile so that it is created when a user is created.
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
"""

class Mooclet(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    external_id = models.IntegerField(null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['organization', 'external_id'], name='unique_mooclet')
        ]
