# Generated by Django 3.2.8 on 2021-12-02 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0003_alter_organization_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='token',
            field=models.CharField(default='db071db130485666bfd39ac15b9dc1eb9d75f9cc', max_length=200),
        ),
    ]
