# Generated by Django 4.1.3 on 2024-01-09 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_alter_poll_poll_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='poll_type',
            field=models.CharField(choices=[('Single', 'Single'), ('Multiple', 'Multiple'), ('Limited', 'Limited')], default='Single', max_length=100),
        ),
    ]
