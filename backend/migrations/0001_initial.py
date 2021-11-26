# Generated by Django 3.2.8 on 2021-11-24 02:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('dateRegistered', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Study',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('dateRegistered', models.DateField()),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.organization')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('secondary_email', models.EmailField(max_length=254, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Mooclet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.IntegerField()),
                ('study', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.study')),
            ],
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permission', models.CharField(choices=[('ADMIN', 'admin'), ('STAFF', 'staff')], max_length=5)),
                ('dateRegistered', models.DateField()),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.organization')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.profile')),
            ],
        ),
    ]
