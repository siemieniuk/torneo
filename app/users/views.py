from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render

from users.forms import CustomUserCreationForm


def register_view(request):
    match (request.method):
        case "GET":
            print(type(request))
            return render(
                request,
                "registration/register.html",
                {"form": CustomUserCreationForm},
            )
        case "POST":
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect("index")
