# Generated by Django 4.2.5 on 2023-10-17 09:08

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('torneo_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discipline',
            name='users_favorite_discipline',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
