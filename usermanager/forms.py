from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from usermanager.models import CustomUser


class RegistrationUserForm(UserCreationForm):
    email = forms.CharField(label="Электронная почта", widget=forms.EmailInput())
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput())
    password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ["email", "password1", "password2"]


class LoginUserForm(AuthenticationForm):
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput())
    remember_me = forms.BooleanField(label="Запомнить меня", required=False)

    class Meta:
        model = CustomUser
        fields = ["email", "password", "remember_me"]


class ChangeUsersNameForm(forms.ModelForm):
    first_name = forms.CharField(label="Имя", required=True)
    last_name = forms.CharField(label="Фамилия", required=True)

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name"]
