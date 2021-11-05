from django.db import models

class Mooclet(models.Model):
    mooclet_name = models.CharField(max_length=100)
    mooclet_id = models.IntegerField(null=True)
    policy_id = models.IntegerField()
