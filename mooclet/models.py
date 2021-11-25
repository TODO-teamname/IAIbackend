from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from commons.models import TimeStampMixin
from backend.models import Study

class Mooclet(models.Model):
    study = models.ForeignKey(Study, on_delete=models.CASCADE)
    external_id = models.IntegerField(null=False)

    def get_url(self) -> str:
        return "url"

    def get_token(self) -> str:
        return "token"
