from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from mooclets.serializers import MoocletSerializer

class OrganizationMoocletSerializer(MoocletSerializer):
    pass
