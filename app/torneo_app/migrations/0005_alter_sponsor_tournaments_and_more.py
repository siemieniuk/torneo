# Generated by Django 4.2.5 on 2023-10-17 16:59

from django.conf import settings
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('torneo_app', '0004_alter_sponsor_logo_alter_sponsor_tournaments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sponsor',
            name='tournaments',
            field=models.ManyToManyField(blank=True, related_name='sponsors', to='torneo_app.tournament'),
        ),
        migrations.AlterField(
            model_name='tournamentassignment',
            name='licence_number',
            field=models.CharField(max_length=16, validators=[django.core.validators.MinLengthValidator(16)]),
        ),
        migrations.AlterUniqueTogether(
            name='tournamentassignment',
            unique_together={('tournament', 'player')},
        ),
    ]