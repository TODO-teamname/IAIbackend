from django.db.models import fields
from django.db.models.fields import files
from rest_framework import serializers
from rest_framework.utils import field_mapping
from .models import Mooclet

class MoocletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mooclet
        fields = ('id', 'mooclet_name', 'mooclet_id', 'policy_id')
