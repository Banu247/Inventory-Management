# Generated by Django 5.0.2 on 2024-07-04 14:02

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventoryapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='returns',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='returns',
            name='reason',
            field=models.TextField(blank=True),
        ),
    ]
