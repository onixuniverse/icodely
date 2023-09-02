from django.contrib import admin

from .models import *


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "description")
    list_display_links = ("title",)
    search_fields = ("title",)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "content")
    list_display_links = ("title", "course")
    search_fields = ("title",)


@admin.register(InviteUrl)
class InviteUrlAdmin(admin.ModelAdmin):
    list_display = ("url", "course", "created_by")
    list_display_links = ("course", "created_by")


@admin.register(UserToCourse)
class UserToCourseAdmin(admin.ModelAdmin):
    list_display = ("invite_uuid", "user", "course")
