from django.contrib import admin

from courses_statistics.models import UserStatistics


@admin.register(UserStatistics)
class InviteUrlAdmin(admin.ModelAdmin):
    list_display = ("user", "lesson", "exam_result", "homework_result", "homework_comment")
    list_display_links = ("user", "lesson", "exam_result", "homework_result", "homework_comment")
