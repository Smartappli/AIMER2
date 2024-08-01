from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from .models import Profile


class LoginForm(forms.Form):
    """Form for user login.

    Fields:
        username (CharField): The user's username.
        password (CharField): The user's password, rendered as a password input.
    """

    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())


class UserRegistrationForm(forms.ModelForm):
    """Form for user registration.

    Fields:
        password (CharField): The user's password, rendered as a password input.
        password2 (CharField): The password confirmation, rendered as a password input.

    Meta:
        model: The user model obtained via get_user_model().
        fields (tuple): The fields to include in the form ("username", "first_name", "last_name", "email").

    Methods
    -------
        clean_password2: Validates that the two password fields match.

    """

    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(),
    )
    password2 = forms.CharField(
        label=_("Confirm Password"),
        widget=forms.PasswordInput(),
    )

    class Meta:
        model = get_user_model()
        fields = ("username", "first_name", "last_name", "email")
        labels = {
            "username": _("Username"),
            "first_name": _("First Name"),
            "last_name": _("Last Name"),
            "email": _("Email"),
        }

    def clean_password2(self):
        """Validate that the password and password confirmation match.

        Raises
        ------
            ValidationError: If the passwords do not match.

        Returns
        -------
            str: The cleaned password confirmation.

        """
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            msg = forms.ValidationError("Passwords don't match")
            raise msg
        return cd["password2"]


class UserEditForm(forms.ModelForm):
    """Form for editing user information.

    Meta:
        model: The user model obtained via get_user_model().
        fields (tuple): The fields to include in the form ("first_name", "last_name", "email").
    """

    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "email")
        labels = {
            "first_name": _("First Name"),
            "last_name": _("Last Name"),
            "email": _("Email"),
        }


class ProfileEditForm(forms.ModelForm):
    """Form for editing user profile information.

    Meta:
        model: The Profile model.
        fields (tuple): The fields to include in the form ("date_of_birth", "photo", "bio").
    """

    class Meta:
        model = Profile
        fields = ("date_of_birth", "photo", "bio")
        labels = {
            "date_of_birth": _("Date of Birth"),
            "photo": _("Profile Photo"),
            "bio": _("Biography"),
        }
