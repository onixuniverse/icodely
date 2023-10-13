from django import forms

from .models import *
from usermanager.models import CustomUser


class ExamAnswerForm(forms.ModelForm):
    answer = forms.CharField()

    class Meta:
        model = ExaminationAnswer
        fields = ["answer"]


class WrongAnswerByUserForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=CustomUser.objects.all().order_by("last_name"))
    exam = forms.ModelChoiceField(queryset=Examination.objects.all())

    class Meta:
        model = CustomUser
        fields = ["id"]
