from django import forms

from .models import *


class AddExaminationAnswerForm(forms.ModelForm):
    class Meta:
        model = ExaminationAnswer
        fields = ["question", "answer"]
