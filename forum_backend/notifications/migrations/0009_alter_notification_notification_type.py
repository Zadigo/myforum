# Generated by Django 4.1.3 on 2024-01-10 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0008_alter_notification_notification_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('Message', 'Message'), ('Follow', 'Follow'), ('Like', 'Like'), ('Shoutout', 'Shoutout')], default='Follow', max_length=50),
        ),
    ]
