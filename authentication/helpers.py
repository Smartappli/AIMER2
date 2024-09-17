from django.conf import settings
from django.core.mail import EmailMessage
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


def send_email(subject, email, message):
    try:
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        email = EmailMessage(subject, message, email_from, recipient_list)
        email.send()
    except Exception as e:
        print(f"Failed to send email: {e}")  # noqa: T201


def get_absolute_url(path):
    return settings.BASE_URL + path


def send_verification_email(email, token):
    subject = _("Verify your email")
    verification_url = get_absolute_url(
        reverse("authentication:auth-verify-email", kwargs={"token": token})
    )
    message = (
        f"Hi,\n\nPlease verify your email using this link: {verification_url}"
    )
    send_email(subject, email, message)


def send_password_reset_email(email, token):
    subject = _("Reset your password")
    reset_url = get_absolute_url(
        reverse("authentication:auth-reset-password", kwargs={"token": token})
    )
    message = f"Hi,\n\nPlease reset your password using this link: {reset_url}"
    send_email(subject, email, message)
