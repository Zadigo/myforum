# Generated by Django 4.0.1 on 2022-06-06 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('threads', '0003_alter_mainthread_category_alter_subthread_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mainthread',
            name='category',
            field=models.CharField(choices=[('General', 'General')], default='General', max_length=50),
        ),
        migrations.AlterField(
            model_name='subthread',
            name='category',
            field=models.CharField(choices=[('General', 'General')], default='General', max_length=50),
        ),
    ]
