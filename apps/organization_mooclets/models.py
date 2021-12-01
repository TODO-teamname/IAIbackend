from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from mooclets.models import MoocletAuthenticator
from organizations.models import Organization
from .permissions import OrganizationExternalMoocletPermissions

class OrganizationMoocletAuthenticator(MoocletAuthenticator):
    organization = models.OneToOneField(Organization, on_delete=models.CASCADE)

    def url(self):
        return self.organization.url

    def token(self):
        return self.organization.token

    def get_permission_classes(self):
        return [OrganizationExternalMoocletPermissions]

@receiver(post_save, sender=Organization)
def create_authenticator(sender, instance, created, **kwargs):
    if created:
        Organization.objects.create(organization=instance)
