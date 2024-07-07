from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from .forms import LoginForm, ProfileEditForm, UserEditForm, UserRegistrationForm
from .models import Profile


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request,
                username=cd["username"],
                password=cd["password"],
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
    return render(request, "website/../templates/registration/login.html", {"forM": form})


@login_required
def dashboard(request):
    return render(
        request,
        'website/dashboard.html',
        {'section': 'dashboard'}
    )


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data["password"])
            # Save th User object
            new_user.save()
            # Create the user profile
            Profile.objects.create(user=new_user)
            return render(
                request,
                "website/register_done.html",
                {"user_form": user_form},
            )
    else:
        user_form = UserRegistrationForm()
    return render(request, "website/register.html", {"user_form": user_form})


@login_required
def edit(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(
        request,
        'website/edit.html',
        {
            'user_form': user_form,
            'profile_form': profile_form,
        }
    )
