# Generated by Django 4.1.3 on 2024-01-10 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('threads', '0008_mainthread_followers_alter_mainthread_category_and_more'),
    ]

    operations = [
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
