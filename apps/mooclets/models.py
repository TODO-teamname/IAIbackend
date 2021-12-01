from typing import List
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from rest_framework.permissions import BasePermissionMetaclass, IsAuthenticated
from django.core.exceptions import FieldError
from .utils.mooclet_connector import MoocletConnector
class MoocletAuthenticator(models.Model):
    class Meta:
        abstract = True

    def get_url(self) -> str:
        raise NotImplementedError

    def get_token(self) -> str:
        raise NotImplementedError

    def get_permission_classes(self) -> List[BasePermissionMetaclass]:
        raise NotImplementedError

class BasicMoocletAuthenticator(MoocletAuthenticator):
    url = models.URLField()
    token = models.CharField(max_length=200)

    def get_url(self):
        return self.url

    def get_token(self):
        return self.token

    def get_permission_classes(self) -> List[BasePermissionMetaclass]:
        return [IsAuthenticated]


class Mooclet(models.Model):
    external_id = models.IntegerField(blank=False)
    name = models.CharField(max_length=200)

    # for abstraction
    authenticator_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, editable=False)
    authenticator_id = models.PositiveIntegerField()
    authenticator_object = GenericForeignKey('authenticator_type', 'authenticator_id')

    def save(self, *args, **kwargs):
        if not isinstance(self.authenticator_object, MoocletAuthenticator):
            raise FieldError("Tried to use an invalid authenticator!")
        super().save(*args, **kwargs)

    @property
    def url(self) -> str:
        return self.authenticator_object.get_url()

    @property
    def token(self) -> str:
        return self.authenticator_object.get_token()

    def get_connector(self) -> MoocletConnector:
        return MoocletConnector(mooclet_id = self.external_id, url = self.url, token = self.token)

    def get_permission_classes(self) -> List[BasePermissionMetaclass]:
        return self.authenticator_object.get_permission_classes()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['authenticator_id', 'external_id'], name='unique_mooclet')
        ]
