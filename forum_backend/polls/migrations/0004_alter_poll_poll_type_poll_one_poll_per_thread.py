# Generated by Django 4.0.1 on 2022-06-06 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_poll_thread_alter_poll_poll_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='poll_type',
            field=models.CharField(choices=[('Single', 'Single'), ('Multiple', 'Multiple'), ('Limited', 'Limited')], default='Single', max_length=100),
        ),
        migrations.AddConstraint(
            model_name='poll',
            constraint=models.UniqueConstraint(fields=('thread',), name='one_poll_per_thread'),
        ),
    ]
