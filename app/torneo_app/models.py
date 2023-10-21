import datetime

from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models
from django.forms import ValidationError

from torneo_app.utils import is_in_future, is_in_past
from users.models import MyUser

# from django.contrib.gis.db import models


class Discipline(models.Model):
    name = models.CharField(max_length=30, unique=True)
    users_favorite_discipline = models.ManyToManyField(MyUser, blank=True)

    def __str__(self):
        return self.name


# TODO: Add geometry
class Tournament(models.Model):
    name = models.CharField(max_length=100)
    applying_deadline = models.DateTimeField(default=datetime.datetime.now)
    max_number_of_participants = models.PositiveIntegerField(
        validators=[MinValueValidator(2)]
    )
    organizer = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    discipline = models.ForeignKey(Discipline, on_delete=models.SET_NULL, null=True)
    sponsors = models.ManyToManyField("Sponsor", related_name="tournaments", blank=True)

    @property
    def applied_participants_count(self):
        how_many_participants = TournamentAssignment.objects.filter(
            tournament=self.pk
        ).count()
        return how_many_participants

    @property
    def has_started(self):
        return is_in_past(self.applying_deadline)

    class Meta:
        indexes = [
            models.Index(fields=["-applying_deadline"]),
            models.Index(fields=["applying_deadline"]),
        ]

    def save(self, *args, **kwargs):
        if is_in_past(self.applying_deadline):
            raise ValidationError("The applying_deadline cannot be in the past!")
        super(Tournament, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Sponsor(models.Model):
    name = models.CharField(max_length=50)
    logo = models.ImageField(upload_to="images/")

    def __str__(self):
        return self.name


class Result(models.Model):
    class Meta:
        unique_together = (("match_id", "tournament"),)

    match_id = models.IntegerField()
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    player_1 = models.ForeignKey(
        MyUser, on_delete=models.SET_NULL, related_name="first_player", null=True
    )
    player_2 = models.ForeignKey(
        MyUser, on_delete=models.SET_NULL, related_name="second_player", null=True
    )
    selected_winner_1 = models.IntegerField(null=True)
    selected_winner_2 = models.IntegerField(null=True)


class TournamentAssignment(models.Model):
    tournament = models.ForeignKey("Tournament", on_delete=models.CASCADE)
    player = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    ranking = models.PositiveIntegerField()
    licence_number = models.CharField(
        max_length=16, validators=[MinLengthValidator(16)]
    )

    class Meta:
        unique_together = (
            ("tournament", "player"),
            ("tournament", "ranking"),
            ("tournament", "licence_number"),
        )

    def save(self, *args, **kwargs):
        if is_in_past(self.tournament.applying_deadline):
            raise ValidationError("Event has started")

        my_assignments = TournamentAssignment.objects.filter(tournament=self.tournament)

        applied = my_assignments.count()
        if applied > self.tournament.max_number_of_participants:
            raise ValidationError("Limit achieved!")
        rankings = set(my_assignments.values_list("ranking"))
        if self.ranking in rankings:
            raise ValidationError("The specified ranking exists among participants")

        super(TournamentAssignment, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.player.email} -> {self.tournament.name}"
