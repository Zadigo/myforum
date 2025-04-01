# Generated by Django 5.0.4 on 2024-05-26 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_alter_permanentban_category_and_more'),
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
            field=models.CharField(choices=[('Racism', 'Racism'), ('Sexism', 'Sexism'), ('Bullying', 'Bullying')], default='Racism', max_length=100),
        ),
        migrations.AlterField(
            model_name='temporaryban',
            name='category',
            field=models.CharField(choices=[('Level 1', 'Level1'), ('Level 2', 'Level2'), ('Level 3', 'Level3')], default='Level 1', max_length=100),
        ),
        migrations.AlterField(
            model_name='temporaryban',
            name='reason',
            field=models.CharField(choices=[('Racism', 'Racism'), ('Sexism', 'Sexism'), ('Bullying', 'Bullying')], default='Racism', max_length=100),
        ),
    ]
