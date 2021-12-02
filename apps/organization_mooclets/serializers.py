from rest_framework import serializers
from django.contrib.auth import get_user_model

from mooclets.serializers import MoocletSerializer, CreateMoocletSerializer
from organizations.models import Organization

class OrganizationMoocletSerializer(MoocletSerializer):
    class Meta(MoocletSerializer.Meta):
        pass

class CreateOrganizationMoocletSerializer(CreateMoocletSerializer):
    def to_internal_value(self, data):
        organization = Organization.objects.get(pk=self.context["organization_pk"])
        self.context["mooclet_authenticator"] = organization.mooclet_authenticator
        return super().to_internal_value(data)
    class Meta(CreateMoocletSerializer.Meta):
        pass
