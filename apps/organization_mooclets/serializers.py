from rest_framework import serializers
from django.contrib.auth import get_user_model

from mooclets.serializers import MoocletSerializer, MoocletCreateSerializer, ExternalMoocletCreateSerializer
from organizations.models import Organization

class OrganizationMoocletSerializer(MoocletSerializer):
    class Meta(MoocletSerializer.Meta):
        pass

class OrganizationMoocletCreateSerializer(MoocletCreateSerializer):
    def to_internal_value(self, data):
        organization = Organization.objects.get(pk=self.context["organization_pk"])
        self.context["mooclet_authenticator"] = organization.mooclet_authenticator
        return super().to_internal_value(data)
    class Meta(MoocletCreateSerializer.Meta):
        pass

class OrganizationExternalMoocletCreateSerializer(serializers.Serializer):
    policy = serializers.IntegerField()
    name = serializers.CharField()
    def to_internal_value(self, data):
        organization = Organization.objects.get(pk=self.context["organization_pk"])
        self.context["mooclet_authenticator"] = organization.mooclet_authenticator
        return super().to_internal_value(data)

    class Meta(ExternalMoocletCreateSerializer.Meta):
        pass

