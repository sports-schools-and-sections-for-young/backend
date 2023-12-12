# Generated by Django 4.2.7 on 2023-12-12 09:28

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
