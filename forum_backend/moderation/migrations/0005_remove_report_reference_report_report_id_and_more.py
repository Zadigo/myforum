# Generated by Django 4.1.3 on 2024-01-08 19:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('moderation', '0004_alter_report_reference'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='reference',
        ),
        migrations.AddField(
            model_name='report',
            name='report_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='usermoderationpreference',
            name='user_to_moderate',
            field=models.ForeignKey(help_text='A user on which the moderation preferences should be applied on', on_delete=django.db.models.deletion.CASCADE, related_name='moderated_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
