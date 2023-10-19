from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from users.models import MyUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ("email", "first_name", "last_name")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = MyUser
        fields = ("email",)
