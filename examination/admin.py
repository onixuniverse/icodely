from django.contrib import admin

from .models import *


@admin.register(Examination)
class ExaminationAdmin(admin.ModelAdmin):
    list_display = ("title", "author")
    list_display_links = ("title",)
    search_fields = ("title",)


@admin.register(ExaminationQuestion)
class ExaminationQuestionAdmin(admin.ModelAdmin):
    list_display = ("exam", "question", "question_image", "right_answer")
    list_display_links = ("exam", "question", "right_answer")
    search_fields = ("exam", "question", "right_answer")


@admin.register(ExaminationAnswer)
class ExaminationAnswerAdmin(admin.ModelAdmin):
    list_display = ("question", "answer", "user")
    list_display_links = ("question", "answer")
    search_fields = ("question",)
