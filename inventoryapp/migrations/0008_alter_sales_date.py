# Generated by Django 5.0.2 on 2024-07-05 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventoryapp', '0007_alter_returns_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sales',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
