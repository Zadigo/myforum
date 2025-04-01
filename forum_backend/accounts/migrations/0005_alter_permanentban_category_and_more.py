# Generated by Django 4.0.1 on 2022-06-06 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_permanentban_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permanentban',
            name='category',
            field=models.CharField(choices=[('Level 1', 'Level1'), ('Level 2', 'Level2'), ('Level 3', 'Level3')], default='Level 1', max_length=100),
        ),
        migrations.AlterField(
            model_name='permanentban',
            name='reason',
            field=models.CharField(choices=[('Racism', 'Racism'), ('Sexism', 'Sexism')], default='Racism', max_length=100),
        ),
        migrations.AlterField(
            model_name='temporaryban',
            name='category',
            field=models.CharField(choices=[('Level 1', 'Level1'), ('Level 2', 'Level2'), ('Level 3', 'Level3')], default='Level 1', max_length=100),
        ),
        migrations.AlterField(
            model_name='temporaryban',
            name='reason',
            field=models.CharField(choices=[('Racism', 'Racism'), ('Sexism', 'Sexism')], default='Racism', max_length=100),
        ),
    ]
