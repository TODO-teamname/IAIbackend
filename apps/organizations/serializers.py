from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from organizations.models import Organization, Membership

class OrganizationSerializer(serializers.ModelSerializer):
    permission_level = serializers.SerializerMethodField(required=False)

    def get_permission_level(self, organization):
        user = self.context['request'].user
        try:
            membership = Membership.objects.get(user=user, organization=organization)
            return membership.permission_level
        except ObjectDoesNotExist:
            return None

    def create(self, validated_data):
        organization = super(OrganizationSerializer, self).create(validated_data)
        organization.members.add(self.context['request'].user, through_defaults={'permission_level': "ADMIN"})
        return organization

    class Meta:
        model=Organization
        fields = ['id', 'token', 'url', 'name', 'permission_level']

        # definitely don't want the token or url to be visible!
        extra_kwargs= {
            'token': {'write_only': True},
            'url': {'write_only': True}
        }


class MembershipSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='user.get_full_name', required=False)
    user = serializers.SlugRelatedField(queryset=get_user_model().objects.all(), slug_field = 'email')

    def create(self, validated_data):
        if Membership.objects.filter(user = validated_data["user"], organization=validated_data["organization_id"]).exists():
            raise serializers.ValidationError("user: That user is already a member of this organization.")

        membership = super(MembershipSerializer, self).create(validated_data)
        return membership

    class Meta:
        model = Membership
        fields = ['id', 'user', 'organization', 'name', 'permission_level']
        extra_kwargs= {
            'organization': {'write_only': True,
                             'required': False},
            'permission_level': {'required': False},
        }


