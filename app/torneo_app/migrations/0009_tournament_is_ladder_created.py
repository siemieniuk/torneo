# Generated by Django 4.2.5 on 2023-12-25 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('torneo_app', '0008_remove_sponsor_tournaments_tournament_sponsors'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='is_ladder_created',
            field=models.BooleanField(default=False),
        ),
    ]
