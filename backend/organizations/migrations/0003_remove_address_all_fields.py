# Generated by Django 3.2.3 on 2023-11-10 18:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0002_address_all_fields'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='all_fields',
        ),
    ]