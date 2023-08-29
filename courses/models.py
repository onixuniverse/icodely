import uuid

from django.contrib.auth.models import User
from django.db import models

from django.urls import reverse


class BackplateCourseColor(models.Model):
    title = models.CharField(max_length=15, verbose_name="Название цвета")
    code_name = models.CharField(max_length=15, verbose_name="Код цвета")


class Course(models.Model):
    title = models.CharField(max_length=63, verbose_name="Название курса")
    description = models.TextField(max_length=255, verbose_name="Описание курса", blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор курса")
    is_available = models.BooleanField(default=True, verbose_name="Курс доступен сразу?")
    price = models.PositiveIntegerField(default=0, verbose_name="Цена за весь курс")
    is_free = models.BooleanField(default=False, verbose_name="Бесплатный курс?")

    backplate_color_choices = [
        ("yellow", "Желтый"),
        ("pink", "Розовый"),
        ("blue", "Голубой"),
        ("gray", "Серый")
    ]
    backplate_color = models.CharField(max_length=6, default="gray", choices=backplate_color_choices,
                                       verbose_name="Цвет фона")

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def get_absolute_url(self):
        return reverse("course", kwargs={'course_id': self.pk})

    def __str__(self):
        return "%s" % self.title

    def save(self, *args, **kwargs):
        self.is_free = False if self.price else True
        super().save(*args, **kwargs)


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.PROTECT, verbose_name="Курс")
    description = models.TextField(max_length=63, verbose_name="Описание шага урока")
    title = models.CharField(max_length=63, verbose_name="Название шага урока")
    content = models.TextField(max_length=4095, verbose_name="Контент шага урока")
    video_youtube = models.CharField(max_length=127, default=None, blank=True, null=True,
                                     verbose_name="Ссылка на видео с Youtube")

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def get_absolute_url(self):
        return reverse("lesson", kwargs={'lesson_id': self.pk, 'course_id': self.course.id})

    def __str__(self):
        return "%s" % self.title


class InviteUrl(models.Model):
    invite_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="UUID ссылки")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, editable=True, verbose_name="Приглашение в курс",
                               blank=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Создатель ссылки")

    class Meta:
        verbose_name = "Приглашение"
        verbose_name_plural = "Приглашения"

    def get_absolute_url(self):
        return reverse("invite", kwargs={"url_uuid": self.pk})

    def __str__(self):
        return "%s" % self.invite_uuid


# Связи моделей
class UserToCourse(models.Model):
    invite_uuid = models.ForeignKey(InviteUrl, on_delete=models.PROTECT, verbose_name="UUID приглашения(ссылки)")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Студент")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс")

    class Meta:
        verbose_name = "Доступ пользователя к курсу"
        verbose_name_plural = "Доступы пользователей к курсам"
