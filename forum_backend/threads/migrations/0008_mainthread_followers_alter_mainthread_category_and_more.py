# Generated by Django 4.1.3 on 2024-01-10 15:48

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('threads', '0007_alter_mainthread_category_alter_subthread_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainthread',
            name='followers',
            field=models.ManyToManyField(blank=True, related_name='main_thread_followers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='mainthread',
            name='category',
            field=models.CharField(choices=[('General discussion', 'General Discussion'), ('Bombshell', 'Bombshell'), ('Result', 'Result'), ('WWW', 'Www'), ('Draw', 'Draw'), ('Poll', 'Poll')], default='General discussion', max_length=50),
        ),
        migrations.AlterField(
            model_name='subthread',
            name='category',
            field=models.CharField(choices=[('General discussion', 'General Discussion'), ('Bombshell', 'Bombshell'), ('Result', 'Result'), ('WWW', 'Www'), ('Draw', 'Draw'), ('Poll', 'Poll')], default='General discussion', max_length=50),
        ),
    ]
