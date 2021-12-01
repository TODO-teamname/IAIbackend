from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from commons.models import TimeStampMixin
from mooclets.models import MoocletAuthenticator

PERMISSION_LEVELS = (
    ("ADMIN", "admin"),
    ("STAFF", "staff")
)

class Organization(TimeStampMixin):
    # Note: maybe implement encryption? Also not THAT important. What is more important is that the server is secure.
    token = models.CharField(max_length=100)
    url = models.URLField(max_length=200)
    name = models.CharField(max_length=100, null=False)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Membership', related_name='organizations')

    def __str__(self):
        return self.name

class Membership(TimeStampMixin):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    permission_level = models.CharField(max_length=100, choices=PERMISSION_LEVELS, default='STAFF')

    def __str__(self):
        return '%s: %s' % (self.user, self.permission_level)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'organization'], name='unique_membership')
        ]
