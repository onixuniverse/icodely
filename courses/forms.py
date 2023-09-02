from django import forms

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
