from rest_framework import serializers

from organizations.models import Organization, Membership

class MembershipSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField(source='user.id')
    organization_id = serializers.ReadOnlyField(source='organization.id')

    def create(self, validated_data):
        self.organization.members.add(user, through_defaults={'permission_level': permission_level})
        return organization

    class Meta:
        model = Membership
        fields = ['user_id', 'organization_id', 'permission_level']
    

class OrganizationSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='user.id', required=False)

    def create(self, validated_data):
        creator = validated_data.pop('creator')
        organization = Organization.objects.create(**validated_data)
        organization.members.add(creator, through_defaults={'permission_level': "ADMIN"})
        return organization

    class Meta:
        model=Organization
        fields = ['id', 'token', 'url', 'name', 'creator']
