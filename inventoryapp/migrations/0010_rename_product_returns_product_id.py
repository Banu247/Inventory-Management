# Generated by Django 5.0.2 on 2024-07-05 01:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventoryapp', '0009_alter_returns_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='returns',
            old_name='product',
            new_name='product_id',
        ),
    ]
