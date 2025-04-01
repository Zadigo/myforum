# Generated by Django 4.0.1 on 2022-06-06 12:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('threads', '0003_alter_mainthread_category_alter_subthread_category'),
        ('polls', '0002_alter_poll_poll_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='thread',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='threads.mainthread'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='poll',
            name='poll_type',
            field=models.CharField(choices=[('Single', 'Single'), ('Multiple', 'Multiple'), ('Limited', 'Limited')], default='Single', max_length=100),
        ),
    ]
