# Generated by Django 5.1.2 on 2024-11-19 11:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preferences', '0004_rename_annual_income_preference_max_annual_income_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='preference',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='preference', to=settings.AUTH_USER_MODEL),
        ),
    ]
