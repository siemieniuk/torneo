from django.contrib import messages
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from users.forms import CustomUserCreationForm
from users.models import MyUser
from users.tokens import account_activation_token


def register_view(request):
    match (request.method):
        case "GET":
            if request.user.is_authenticated:
                return redirect("my_page")
            return render(
                request,
                "registration/register.html",
                {"form": CustomUserCreationForm},
            )
        case "POST":
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = False
                user.save()

                current_site = get_current_site(request)
                mail_subject = "Torneo: Activation link"
                message = render_to_string(
                    "activation_mail.html",
                    {
                        "user": user,
                        "domain": current_site.domain,
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "token": account_activation_token.make_token(user),
                    },
                )
                recipient = form.cleaned_data.get("email")
                email = EmailMessage(mail_subject, message, to=[recipient])
                email.send()
                return render(
                    request,
                    "registration/activation_mail_sent.html",
                    {"email": user.email},
                )


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = MyUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, MyUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, "Successfully confirmed your email account!")
        return redirect("my_page")
    else:
        messages.error(request, "Activation link is invalid!")
        return redirect("login")
