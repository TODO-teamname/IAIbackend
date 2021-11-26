from rest_framework import serializers, validators
from django.contrib.auth import get_user_model


from organizations.models import Organization, Membership

class MembershipSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='user.get_full_name', required=False)
    user = serializers.SlugRelatedField(queryset=get_user_model().objects.all(), slug_field = 'email')

    def create(self, validated_data):
        if Membership.objects.filter(user = validated_data["user"], organization = validated_data["organization_id"]).exists():
            raise serializers.ValidationError("message: That user is already a member of this organization.")

        membership = super(MembershipSerializer, self).create(validated_data)
        return membership

    class Meta:
        model = Membership
        fields = ['id', 'user', 'organization', 'name', 'permission_level']
        extra_kwargs= {
            'organization': {'write_only': True,
                             'required': False},
        }

class OrganizationSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        organization = super(OrganizationSerializer, self).create(validated_data)
        organization.members.add(self.context['request'].user, through_defaults={'permission_level': "ADMIN"})
        return organization

    class Meta:
        model=Organization
        fields = ['id', 'token', 'url', 'name']
