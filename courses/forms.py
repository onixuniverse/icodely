from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import MinLengthValidator

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
    username = forms.CharField(label="Логин", widget=forms.TextInput(), validators=[
        MinLengthValidator(6, message="Имя пользователя должно состоять минимум из 6 символов.")
    ])
    email = forms.CharField(label="Электронная почта", widget=forms.EmailInput())
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput())
    password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput(), validators=[
        MinLengthValidator(6, message="Имя пользователя должно состоять минимум из 6 символов.")
    ])
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput())
    remember_me = forms.BooleanField(label="Запомнить меня", required=False)

    class Meta:
        model = User
        fields = ["username", "password", "remember_me"]
