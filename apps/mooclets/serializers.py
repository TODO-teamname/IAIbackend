from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Mooclet, MoocletAuthenticator
from mooclets.utils.mooclet_connector import MoocletCreator

class MoocletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mooclet
        fields = ['id', 'external_id', 'name', 'policy']

# for internal use
class MoocletCreateSerializer(MoocletSerializer):
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
            raise ValidationError("external_id: Mooclet Already Exists")
        super().validate(data)

        return data

    def to_internal_value(self, data):
        content_object = self.context["mooclet_authenticator"]
        ret = super().to_internal_value(data)
        ret['content_object'] = content_object
        return ret

    class Meta(MoocletSerializer.Meta):
        write_only_fields = ('content_object')

class ExternalMoocletCreateSerializer():
    def validate_content_object(self, value):
        if not isinstance(value, MoocletAuthenticator):
            raise ValueError("passed in an invalid authenticator during mooclet creation")
        return value

    def validate(self, data):
        content_object = self.context["mooclet_authenticator"]
        self.validate_content_object(content_object)

        super().validate(data)

        return data

    def to_internal_value(self, data):
        content_object = self.context["mooclet_authenticator"]
        ret = super().to_internal_value(data)
        ret['content_object'] = content_object
        return ret

    def create(self, validated_data):
        content_object = validated_data.pop("content_object")
        policy_id = validated_data.pop("policy_id")
        mooclet_name = validated_data.pop("mooclet_name")
        mooclet_creator = content_object.get_mooclet_creator()
        mooclet_data = mooclet_creator.create(policy=policy_id, name=mooclet_name)
        return Mooclet(content_object=content_object, external_id=mooclet_data["id"])

    class Meta(MoocletSerializer.Meta):
        write_only_fields = ('content_object')
        optional_fields = ('external_id')


class VersionSerializer(serializers.Serializer):
    version_name = serializers.CharField(source='name')
    version_text = serializers.CharField(source='text')
    version_json = serializers.JSONField()


class PolicyParameterSerializer(serializers.Serializer):
    policy_id = serializers.IntegerField(source='policy')
    policy_parameters = serializers.JSONField(source='parameters')

class VariableSerializer(serializers.Serializer):
    variable_name = serializers.CharField(source='name')

class DownloadVarNamesSerializer(serializers.Serializer):
    reward = serializers.CharField()
    policy = serializers.IntegerField()
