from captcha import fields, widgets
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from usermanager.models import CustomUser


class UserRegistrationForm(UserCreationForm):
    email = forms.CharField(label="Электронная почта", widget=forms.EmailInput())
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput())
    password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput)
    captcha = fields.ReCaptchaField(widget=widgets.ReCaptchaV3())

    class Meta:
        model = CustomUser
        fields = ["email", "password1", "password2", "captcha"]


class UserLoginForm(AuthenticationForm):
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput())
    captcha = fields.ReCaptchaField(label="", widget=widgets.ReCaptchaV3())
    remember_me = forms.BooleanField(label="Запомнить меня", required=False)

    class Meta:
        model = CustomUser
        fields = ["email", "password", "remember_me", "captcha"]


class ChangeUsersNameForm(forms.ModelForm):
    first_name = forms.CharField(label="Имя", required=True)
    last_name = forms.CharField(label="Фамилия", required=True)

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name"]
