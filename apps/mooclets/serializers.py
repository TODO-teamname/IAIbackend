from django.db.models import fields
from django.db.models.fields import files
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.utils import field_mapping
from .models import Mooclet, MoocletAuthenticator
from backend.utils.mooclet_connector import MoocletCreator

class MoocletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mooclet
        fields = ['id', 'external_id', 'name']


# for internal use
class CreateMoocletSerializer(MoocletSerializer):
    def validate_content_object(self, value):
        if not isinstance(value, MoocletAuthenticator):
            raise ValueError("passed in an invalid authenticator during mooclet creation")
        return value

    def validate(self, data):
        content_object = self.context["mooclet_authenticator"]
        self.validate_content_object(content_object)
        content_type = ContentType.objects.get_for_model(content_object)
        external_id = data["external_id"]

        if Mooclet.objects.filter(object_id=content_object.id, content_type=content_type, external_id=external_id).exists():
            raise ValidationError("mooclet: Mooclet Already Exists")
        super().validate(data)

        return data

    def to_internal_value(self, data):
        content_object = self.context["mooclet_authenticator"]
        ret = super().to_internal_value(data)
        ret['content_object'] = content_object
        return ret


    class Meta(MoocletSerializer.Meta):
        write_only_fields = ('content_object')

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
