from django import forms

from courses_statistics.models import UserStatistics


class UploadHomeworkFile(forms.ModelForm):
    homework_upload_file = forms.FileField()

    class Meta:
        model = UserStatistics
        fields = ["homework_upload_file"]
