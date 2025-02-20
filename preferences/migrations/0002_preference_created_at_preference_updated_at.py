# Generated by Django 5.1.2 on 2024-11-15 05:44

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preferences', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='preference',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='preference',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
