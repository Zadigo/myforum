# Generated by Django 5.0.6 on 2024-12-11 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0012_alter_notification_notification_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('Message', 'Message'), ('Follow', 'Follow'), ('Like', 'Like'), ('Shoutout', 'Shoutout')], default='Follow', max_length=50),
        ),
    ]
