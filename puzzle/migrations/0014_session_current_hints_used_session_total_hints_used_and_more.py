# Generated by Django 4.2.6 on 2023-10-29 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('puzzle', '0013_rename_creator_session_player'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='current_hints_used',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='session',
            name='total_hints_used',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='session',
            name='total_score',
            field=models.IntegerField(default=0),
        ),
    ]