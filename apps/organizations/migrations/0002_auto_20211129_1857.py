# Generated by Django 3.2.8 on 2021-11-29 18:57

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organizations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='permission_level',
            field=models.CharField(choices=[('ADMIN', 'admin'), ('STAFF', 'staff')], default='STAFF', max_length=100),
        ),
        migrations.AlterField(
            model_name='organization',
            name='members',
            field=models.ManyToManyField(related_name='organizations', through='organizations.Membership', to=settings.AUTH_USER_MODEL),
        ),
    ]
