from captcha.fields import CaptchaField
from django import forms


class AxesCaptchaForm(forms.Form):
    captcha = CaptchaField()
