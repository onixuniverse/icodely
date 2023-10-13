from django import forms

from courses_statistics.models import UserStatistics


class UploadHomeworkFile(forms.ModelForm):
    class Meta:
        model = UserStatistics
        fields = ["homework_upload_file"]
