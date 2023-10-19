import datetime

from django import forms

from torneo_app.models import Tournament, TournamentAssignment


class TournamentCreateForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = (
            "name",
            "applying_deadline",
            "max_number_of_participants",
        )

    def clean(self):
        cleaned_data = super().clean()
        applying_deadline = cleaned_data.get("applying_deadline", "")
        if applying_deadline < datetime.datetime.now():
            raise forms.ValidationError("date in the past")
        return cleaned_data


class TournamentApplyForm(forms.ModelForm):
    class Meta:
        model = TournamentAssignment
        fields = ("ranking", "licence_number")
