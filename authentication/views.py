import uuid
from datetime import timedelta, timezone

from axes.utils import reset_request
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import Group, User
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

from AIMER2 import TemplateLayout
from AIMER2.template_helpers.theme import TemplateHelper
from authentication.helpers import (
    send_password_reset_email,
    send_verification_email,
)
from authentication.models import Profile

from .forms import AxesCaptchaForm


class AuthView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in AIMER2/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        # Update the context
        context.update({
            "layout_path": TemplateHelper.set_layout(
                "layout_blank.html", context
            ),
        })

        return context


class LoginView(AuthView):
    def get(self, request):
        if request.user.is_authenticated:
            # If the user is already logged in, redirect them to the home page or another appropriate page.
            return redirect("website:index")

        # Render the login page for users who are not logged in.
        return super().get(request)

    def post(self, request):  # noqa: RET503
        if request.method == "POST":
            username = request.POST.get("email-username")
            password = request.POST.get("password")

            if not (username and password):
                messages.error(
                    request, _("Please enter your username and password.")
                )
                return redirect("authentication:auth-login")

            if "@" in username:
                user_email = User.objects.filter(email=username).first()
                if user_email is None:
                    messages.error(request, _("Please enter a valid email."))
                    return redirect("authentication:auth-login")
                username = user_email.username

            user_email = User.objects.filter(username=username).first()
            if user_email is None:
                messages.error(request, _("Please enter a valid username."))
                return redirect("authentication:auth-login")

            authenticated_user = authenticate(
                request=request,  # this is the important custom argument
                username=username,
                password=password,
            )
            if authenticated_user is not None:
                # Ensure the user has a profile
                if not hasattr(authenticated_user, "profile"):
                    Profile.objects.create(user=authenticated_user)

                if not authenticated_user.password.startswith(
                    "argon2$"
                ) and check_password(password, authenticated_user.password):
                    # Re-hasher with Argon2 or more recent algorithm
                    authenticated_user.password = make_password(password)
                    authenticated_user.save()

                # Login the user if authentication is successful
                login(request, authenticated_user)

                # Redirect to the page the user was trying to access before logging in
                if "next" in request.POST:
                    return redirect(request.POST["next"])

                # Redirect to the home page or another appropriate page
                return redirect("website:index")

            messages.error(request, _("Please enter a valid username."))
            return redirect("authentication:auth-login")


class LogoutView(AuthView):
    def post(self, request):
        if request.user.is_authenticated:
            logout(request)
            return redirect("authentication:auth-logout")
        return None


class RegisterView(AuthView):
    def get(self, request):
        if request.user.is_authenticated:
            # If the user is already logged in, redirect them to the home page or another appropriate page.
            return redirect(
                "website:index"
            )  # Replace 'index' with the actual URL name for the home page

        # Render the login page for users who are not logged in.
        return super().get(request)

    def post(self, request):
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Check if a user with the same username or email already exists
        if User.objects.filter(username=username, email=email).exists():
            messages.error(request, _("User already exists, Try logging in."))
            return redirect("authentication:auth-register")
        if User.objects.filter(email=email).exists():
            messages.error(request, _("Email already exists."))
            return redirect("authentication:auth-register")
        if User.objects.filter(username=username).exists():
            messages.error(request, _("Username already exists."))
            return redirect("authentication:auth-register")

        # Create the user and set their password
        created_user = User.objects.create_user(
            username=username, email=email, password=password
        )
        created_user.set_password(password)
        created_user.save()

        # Add the user to the 'client' group (or any other group you want to use as default for new users)
        user_group, _created = Group.objects.get_or_create(name="client")
        created_user.groups.add(user_group)

        # Generate a token and send a verification email here
        token = str(uuid.uuid4())

        # Set the token in the user's profile
        user_profile, _created = Profile.objects.get_or_create(
            user=created_user
        )
        user_profile.email_token = token
        user_profile.email = email
        user_profile.save()

        send_verification_email(email, token)

        if settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD:
            messages.success(request, _("Verification email sent successfully"))
        else:
            messages.error(
                request,
                _(
                    "Email settings are not configured. Unable to send verification email."
                ),
            )

        request.session["email"] = email  # Save email in session
        # Redirect to the verification page after successful registration
        return redirect("authentication:auth-verify-email-page")


class ForgetPasswordView(AuthView):
    def get(self, request):
        if request.user.is_authenticated:
            # If the user is already logged in, redirect them to the home page or another appropriate page.
            return redirect(
                "website:index"
            )  # Replace 'index' with the actual URL name for the home page

        # Render the login page for users who are not logged in.
        return super().get(request)

    def post(self, request):
        if request.method == "POST":
            email = request.POST.get("email")

            user = User.objects.filter(email=email).first()
            if not user:
                messages.error(request, _("No user with this email exists."))
                return redirect("authentication:auth-forgot-password")

            # Generate a token and send a password reset email here
            token = str(uuid.uuid4())

            # Set the token in the user's profile and add an expiration time (e.g., 24 hours from now)
            expiration_time = timezone.now() + timedelta(hours=24)

            user_profile, _created = Profile.objects.get_or_create(user=user)
            user_profile.forget_password_token = token
            user_profile.forget_password_token_expiration = expiration_time
            user_profile.save()

            # Send the password reset email
            send_password_reset_email(email, token)

            if settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD:
                messages.success(
                    request,
                    _(
                        "A password reset email has been sent. Please check your inbox"
                    ),
                )
            else:
                messages.error(
                    request,
                    _(
                        "Email settings are not configured. Unable to send verification email."
                    ),
                )

            return redirect("authentication:auth-forgot-password")
        return None


class ResetPasswordView(AuthView):
    def get(self, request, token):
        if request.user.is_authenticated:
            # If the user is already logged in, redirect them to the home page or another appropriate page.
            return redirect("website:index")

        # Render the login page for users who are not logged in.
        return super().get(request)

    def post(self, request, token):
        try:
            profile = Profile.objects.get(forget_password_token=token)
        except Profile.DoesNotExist:
            messages.error(request, _("Invalid or expired token."))
            return redirect("authentication:auth-forgot-password")

        if request.method == "POST":
            new_password = request.POST.get("password")
            confirm_password = request.POST.get("confirm-password")

            if not (new_password and confirm_password):
                messages.error(request, _("Please fill all fields."))
                return render(request, "auth/reset_password.html")

            if new_password != confirm_password:
                messages.error(request, "Passwords do not match.")
                return render(request, "auth/reset_password.html")

            user = profile.user
            user.set_password(new_password)
            user.save()

            # Clear the forget_password_token
            profile.forget_password_token = ""
            profile.save()

            # Log the user in after a successful password reset
            authenticated_user = authenticate(
                request=request,  # this is the important custom argument
                username=user.username,
                password=new_password,
            )
            if authenticated_user:
                login(request, authenticated_user)
                return redirect("website:index")
            messages.success(
                request, _("Password reset successful. Please log in.")
            )
            return redirect("authentication:auth-login")
        return None


class VerifyEmailTokenView(AuthView):
    def get(self, request, token):
        try:
            profile = Profile.objects.filter(email_token=token).first()
            profile.is_verified = True
            profile.email_token = ""
            profile.save()
            if not request.user.is_authenticated:
                # User is not already authenticated
                # Perform the email verification and any other necessary actions
                messages.success(request, _("Email verified successfully"))
            return redirect("authentication:auth-login")
            # Now, redirect to the login page

        except Profile.DoesNotExist:
            messages.error(request, _("Invalid token, please try again"))
            return redirect("authentication:auth-verify-email-page")


class VerifyEmailView(AuthView):
    def get(self, request):
        # Render the login page for users who are not logged in.
        return super().get(request)


class SendVerificationView(AuthView):
    def get(self, request):
        email, message = self.get_email_and_message(request)

        if email:
            token = str(uuid.uuid4())
            user_profile = Profile.objects.filter(email=email).first()
            user_profile.email_token = token
            user_profile.save()
            send_verification_email(email, token)
            messages.success(request, message)
        else:
            messages.error(request, _("Email not found in session"))

        return redirect("authentication:auth-verify-email-page")

    def get_email_and_message(self, request):
        if request.user.is_authenticated:
            email = request.user.profile.email

            if settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD:
                message = messages.success(
                    request, _("Verification email sent successfully")
                )
            else:
                message = messages.error(
                    request,
                    _(
                        "Email settings are not configured. Unable to send verification email."
                    ),
                )
        else:
            email = request.session.get("email")
            if settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD:
                message = (
                    _("Resend verification email successfully")
                    if email
                    else None
                )
            else:
                message = messages.error(
                    request,
                    _(
                        "Email settings are not configured. Unable to send verification email."
                    ),
                )

        return email, message


class LockedOutView(AuthView):
    def post(self, request):
        if request.POST:
            form = AxesCaptchaForm(request.POST)
            if form.is_valid():
                reset_request(request)
                return HttpResponseRedirect(
                    reverse_lazy("authentication:auth-login")
                )
        else:
            form = AxesCaptchaForm()

        return render(request, "auth/captcha.html", {"form": form})


def locked_out(request):
    if request.POST:
        form = AxesCaptchaForm(request.POST)
        if form.is_valid():
            reset_request(request)
            return HttpResponseRedirect(
                reverse_lazy("authentication:auth-login")
            )
    else:
        form = AxesCaptchaForm()

    return render(request, "auth/captcha.html", {"form": form})
