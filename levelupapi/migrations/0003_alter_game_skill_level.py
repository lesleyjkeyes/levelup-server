# Generated by Django 4.1.3 on 2022-11-22 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('levelupapi', '0002_alter_game_maker'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='skill_level',
            field=models.CharField(max_length=50),
        ),
    ]