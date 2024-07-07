from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from .forms import LoginForm, UserRegistrationForm


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, username=cd["username"], password=cd["password"],
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse(
                        "Authenticated and logged in successfully",
                    )
                else:
                    return HttpResponse("Inactive user login")
            else:
                return HttpResponse("Invalid login or password")
    else:
        form = LoginForm()
    return render(request, "website/login.html", {"forM": form},)


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data["password"])
            new_user.save()
            return render(
                request, "website/register_done.html", {"user_form": user_form},
            )
    else:
        user_form = UserRegistrationForm()
    return render(request, "account/register.html", {"user_form": user_form})
