from typing import List
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from rest_framework.permissions import BasePermissionMetaclass, IsAuthenticated
from django.core.exceptions import FieldError
from .utils.mooclet_connector import MoocletConnector


class Mooclet(models.Model):
    external_id = models.IntegerField(blank=False)
    name = models.CharField(max_length=200)

    # for abstraction
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, editable=False)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    @property
    def url(self) -> str:
        return self.content_object.get_url()

    @property
    def token(self) -> str:
        return self.content_object.get_token()

    def get_connector(self) -> MoocletConnector:
        return MoocletConnector(mooclet_id = self.external_id, url = self.url, token = self.token)

    def get_permission_classes(self) -> List[BasePermissionMetaclass]:
        return self.content_object.get_permission_classes()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['content_type', 'object_id', 'external_id'], name='unique_mooclet_for_authenticator')
        ]

class MoocletAuthenticator(models.Model):
    # NOTE: something like this would be better, but for some reason migrations aren't working
    #mooclets = GenericRelation(Mooclet, related_query_name='mooclet_authenticator')
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

