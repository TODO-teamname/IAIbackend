from django.db.models import fields
from django.db.models.fields import files
from rest_framework import serializers
from rest_framework.utils import field_mapping
from .models import Mooclet
from .utils.mooclet_connector import MoocletCreator

class MoocletSerializer(serializers.ModelSerializer):
    authenticator = serializers.IntegerField()

    def create():
        pass

    class Meta:
        model = Mooclet
        fields = ['id', 'external_id', 'name']

class APICallSerializer(serializers.Serializer):
    mooclet = MoocletSerializer()
    # Did not add thorough validation for fields, change to NotImplementedError
    def validate(self):
        return True

class VersionSerializer(APICallSerializer):
    version_name = serializers.CharField()
    version_json = serializers.JSONField()

class CreateExternalMoocletSerializer(serializers.ModelSerializer):
    policy_id = serializers.IntegerField()

    def validate_policy_id(self, data):
        if data['policy_id'] < 0:
            raise serializers.ValidationError("oh no")

    def create(self, validated_data):
        organization = Organization.objects.get(organization=validated_data['organization'])
        token = organization.token
        url = organization.url

        new_id, mooclet_info = MoocletCreator(token, url, validated_data['mooclet_name'], validated_data['policy_id']).create_mooclet()
        mooclet = Mooclet(new_id, validated_data['mooclet_name'], validated_data["organization"])
        mooclet.save()
        return mooclet

        
    class Meta:
        model = Mooclet
        fields = ('id', 'mooclet_name', 'external_id', 'organization')
        extra_kwargs = {
            'organization': {'write_only': True},
            'external_id': {'write_only': True},
        }
