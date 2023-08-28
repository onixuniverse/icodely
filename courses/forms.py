from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import *


class AddCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["title", "description"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-input"}),
            "description": forms.Textarea(attrs={"cols": 60, "rows": 10})
        }


class AddLessonForm(forms.ModelForm):
    videos = forms.FileField(label="Видео")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.fields["course"].empty_label = "Курс не выбран"
        self.fields["course"].queryset = Course.objects.filter(author=user.id)

    class Meta:
        model = Lesson
        fields = ["course", "title", "content", "videos"]


class RegistrationUserForm(UserCreationForm):
    username = forms.CharField(label="Логин")
    email = forms.CharField(label="Электронная почта")
    password1 = forms.CharField(label="Пароль")
    password2 = forms.CharField(label="Подтверждение пароля")

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        widgets = {
            "username": forms.TextInput(),
            "email": forms.EmailInput(),
            "password1": forms.PasswordInput(),
            "password2": forms.PasswordInput()
        }


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput())
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput())
    remember_me = forms.BooleanField(label="Запомнить меня", required=False)
