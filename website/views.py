from django.contrib import messages
from django.contrib.auth import alogin, authenticate
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.views.generic.edit import FormView
from web_project import TemplateLayout
from web_project.template_helpers.theme import TemplateHelper

from .forms import (
    LoginForm,
    ProfileEditForm,
    UserEditForm,
    UserRegistrationForm,
)
from .models import Profile


class WebsiteView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        # Update the context
        context.update(
            {
                "layout_path": TemplateHelper.set_layout(
                    "layout_blank.html",
                    context,
                ),
            },
        )

        return context


class CustomLoginView(WebsiteView, auth_views.LoginView):
    template_name = "registration/login.html"


class CustomLogoutView(WebsiteView, auth_views.LogoutView):
    template_name = "registration/logged_out.html"


class CustomPasswordChangeView(WebsiteView, auth_views.PasswordChangeView):
    template_name = "registration/password_change_form.html"


class CustomPasswordChangeDoneView(
    WebsiteView,
    auth_views.PasswordChangeDoneView,
):
    template_name = "registration/password_change_done.html"


class CustomPasswordResetView(WebsiteView, auth_views.PasswordResetView):
    template_name = "registration/password_reset_form.html"


class CustomPasswordResetDoneView(
    WebsiteView,
    auth_views.PasswordResetDoneView,
):
    template_name = "registration/password_reset_done.html"


class CustomPasswordResetConfirmView(
    WebsiteView,
    auth_views.PasswordResetConfirmView,
):
    template_name = "registration/password_reset_confirm.html"


class CustomPasswordResetCompleteView(
    WebsiteView,
    auth_views.PasswordResetCompleteView,
):
    template_name = "registration/password_reset_complete.html"


def user_login(request):
    """Handle user login functionality.

    If the request method is POST, authenticate the user using the provided credentials.
    If authentication is successful and the user is active, log the user in and return
    a success message. If the user is inactive or the credentials are invalid, return
    an appropriate error message. If the request method is GET, display the login form.

    Args:
    ----
        request (HttpRequest): The HTTP request object containing metadata about the request.

    Returns:
    -------
        HttpResponse: A response object with the rendered login form or a success/error message.

    """
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
                    alogin(request, user)
                    return HttpResponse(
                        "Authenticated and logged in successfully",
                    )
                return HttpResponse("Inactive user login")
            return HttpResponse("Invalid login or password")
    else:
        form = LoginForm()
    return render(
        request,
        "registration/login.html",
        {"form": form},
    )


@login_required
def dashboard(request):
    """Display the user dashboard.

    This view is only accessible to authenticated users. It renders the dashboard
    template with the 'section' context variable set to 'dashboard'.

    Args:
    ----
        request (HttpRequest): The HTTP request object containing metadata about the request.

    Returns:
    -------
        HttpResponse: A response object with the rendered dashboard template.

    """
    return render(
        request,
        "website/dashboard.html",
        {"section": "dashboard"},
    )


class CustomRegisterView(WebsiteView, FormView):
    template_name = "website/register.html"
    form_class = UserRegistrationForm

    def form_valid(self, form):
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data["password"])
        new_user.save()
        Profile.objects.create(user=new_user)
        return render(
            self.request, "website/register_done.html", {"user_form": form}
        )


class CustomEditView(WebsiteView, View):
    template_name = "website/edit.html"

    def get(self, request):
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        return render(
            request,
            self.template_name,
            {
                "user_form": user_form,
                "profile_form": profile_form,
            },
        )

    def post(self, request):
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES,
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully!")
        else:
            messages.error(request, "Error updating profile!")
        return render(
            request,
            self.template_name,
            {
                "user_form": user_form,
                "profile_form": profile_form,
            },
        )
