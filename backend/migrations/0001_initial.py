# Generated by Django 3.2.8 on 2021-11-05 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mooclet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mooclet_name', models.CharField(max_length=100)),
                ('mooclet_id', models.IntegerField(null=True)),
                ('policy_id', models.IntegerField()),
            ],
        ),
    ]
