from django import forms

from .models import *


class ExamAnswerForm(forms.ModelForm):
    answer = forms.CharField()

    class Meta:
        model = ExaminationAnswer
        fields = ["answer"]
