from django import forms

from torneo_app.models import Result, Tournament, TournamentAssignment
from torneo_app.utils import is_in_past


class TournamentModelForm(forms.ModelForm):
    class Meta:
        model = Tournament
        exclude = ("organizer", "is_ladder_created")

    def __init__(self, *args, **kwargs):
        self.organizer = kwargs.pop("organizer", None)
        self.update = kwargs.pop("update", False)
        super(TournamentModelForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        applying_deadline = cleaned_data.get("applying_deadline", "")
        if not self.update and is_in_past(applying_deadline):
            raise forms.ValidationError("date in the past")
        return cleaned_data

    def save(self, commit=True):
        instance = super(TournamentModelForm, self).save(commit=False)
        instance.organizer = self.organizer
        if commit:
            instance.save(updated=self.update)
        return instance


class TournamentApplyForm(forms.ModelForm):
    class Meta:
        model = TournamentAssignment
        fields = ("ranking", "licence_number")

    def __init__(self, *args, **kwargs):
        self.tournament = kwargs.pop("tournament", None)
        self.applying_user = kwargs.pop("applying_user", None)
        super(TournamentApplyForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        ranking = cleaned_data.get("ranking", 0)
        if ranking < 0:
            raise forms.ValidationError("Ranking cannot be negative")
        return cleaned_data

    def save(self, commit=True):
        instance = super(TournamentApplyForm, self).save(commit=False)
        instance.tournament = self.tournament
        instance.player = self.applying_user
        if commit:
            instance.save()
        return instance


class ResultForm(forms.ModelForm):
    chosen_result = forms.ChoiceField(
        widget=forms.RadioSelect,
        label="Who has won the match?",
    )

    class Meta:
        model = Result
        fields = ()

    def __init__(self, *args, **kwargs):
        self.user_id = kwargs.pop("user", None)
        super(ResultForm, self).__init__(*args, **kwargs)
        choices = (
            ("1", self.instance.player_1),
            ("2", self.instance.player_2),
        )
        self.fields["chosen_result"].choices = choices

    def clean(self):
        cleaned_data = super().clean()
        self.selected_option = cleaned_data.get("chosen_result", None)
        if self.selected_option not in ("1", "2"):
            raise forms.ValidationError("Incorrect option!")

        cleaned_data["chosen_result"] = dict(
            self.fields["chosen_result"].choices
        )[self.selected_option].id

        for key, val in self.fields["chosen_result"].choices:
            if val.id == self.user_id:
                self.option_to_update = key
                self.user_as_new_value = cleaned_data["chosen_result"]
                print(self.user_as_new_value)
                break
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        # TODO: Should update selected winner based on user_id; this code is wrong
        if self.option_to_update == "1":
            instance.selected_winner_1 = self.user_as_new_value
        else:
            instance.selected_winner_2 = self.user_as_new_value

        if (
            instance.selected_winner_1 != instance.selected_winner_2
            and instance.selected_winner_1 is not None
            and instance.selected_winner_2 is not None
        ):
            instance.selected_winner_1 = None
            instance.selected_winner_2 = None

        if commit:
            instance.save()
        return instance
