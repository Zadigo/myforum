# Generated by Django 4.0.1 on 2022-06-06 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forums', '0002_alter_forum_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forum',
            name='category',
            field=models.CharField(choices=[('General', 'General'), ('News', 'News'), ('Miscellaneous', 'Miscellaneous')], default='General', help_text='Used to regroup forums of a same category together', max_length=50),
        ),
    ]
