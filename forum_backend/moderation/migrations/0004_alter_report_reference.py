# Generated by Django 4.0.1 on 2022-06-06 12:57

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('moderation', '0003_alter_report_reference'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='reference',
            field=models.UUIDField(default=uuid.UUID('a26a8ace-d834-486e-80fb-1a100c851b56')),
        ),
    ]
