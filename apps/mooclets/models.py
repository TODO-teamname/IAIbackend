from typing import List
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from rest_framework.permissions import BasePermissionMetaclass, IsAuthenticated
from django.core.exceptions import FieldError
from backend.utils.mooclet_connector import MoocletConnector, MoocletCreator


class Mooclet(models.Model):
    external_id = models.IntegerField(blank=False)

    # for abstraction
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, editable=False)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    mooclet_data = None

    @property
    def url(self) -> str:
        return self.content_object.get_url()

    @property
    def token(self) -> str:
        return self.content_object.get_token()

    def get_connector(self) -> MoocletConnector:
        return MoocletConnector(mooclet_id=self.external_id, url=self.url, token=self.token)

    # NOTE: intention here is to minimize external API calls
    def get_data(self):
        if not self.mooclet_data:
            mooclet_connector = self.get_connector()
            self.mooclet_data = mooclet_connector.get_mooclet()
        return self.mooclet_data

    @property
    def name(self):
        return self.get_data()["name"]

    @property
    def policy(self):
        return self.get_data()["policy"]

    @property
    def parameters(self):
        return self.get_data()["parameters"]

    def get_permission_classes(self) -> List[BasePermissionMetaclass]:
        return self.content_object.get_permission_classes()

    def save(self, *args, **kwargs):
        mooclet_connector = self.get_connector()
        mooclet_connector.check_mooclet()
        super().save(*args, **kwargs)

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

    def get_mooclet_creator(self) -> MoocletCreator:
        return MoocletCreator(url=self.get_url(), token=self.get_token())

class BasicMoocletAuthenticator(MoocletAuthenticator):
    url = models.URLField()
    token = models.CharField(max_length=200)

    def get_url(self):
        return self.url

    def get_token(self):
        return self.token

    def get_permission_classes(self) -> List[BasePermissionMetaclass]:
        return [IsAuthenticated]

