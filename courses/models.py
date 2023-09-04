import uuid

from django.db import models

from django.urls import reverse

from usermanager.models import CustomUser


class BackplateCourseColor(models.Model):
    title = models.CharField(max_length=15, verbose_name="Название цвета")
    code_name = models.CharField(max_length=15, verbose_name="Код цвета")


class Course(models.Model):
    title = models.CharField(max_length=63, verbose_name="Название курса")
    # short_description
    description = models.TextField(max_length=1023, verbose_name="Описание курса", blank=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Автор курса")
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
    # short_description
    description = models.TextField(max_length=1023, verbose_name="Описание шага урока")
    title = models.CharField(max_length=63, verbose_name="Название шага урока")
    content = models.TextField(max_length=4095, verbose_name="Контент шага урока")
    video_youtube = models.CharField(max_length=127, default=None, blank=True, null=True,
                                     verbose_name="Ссылка на видео с Youtube")
    pdf_file = models.FileField(upload_to="uploads/lessons/pdf/", default=None, null=True, blank=True,
                                verbose_name="PDF-файл")

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def get_absolute_url(self):
        return reverse("lesson", kwargs={'lesson_id': self.pk, 'course_id': self.course.id})

    def __str__(self):
        return "%s" % self.title


class InviteUrl(models.Model):
    invite_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="UUID")
    url = models.CharField(max_length=127, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, editable=True, verbose_name="Курс",
                               blank=False)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Создатель ссылки")

    def __init__(self, *args, **kwargs):
        super(InviteUrl, self).__init__(*args, **kwargs)
        self.url = "https://icodely.ru/invite?url=" + str(self.invite_uuid)

    class Meta:
        verbose_name = "Приглашение"
        verbose_name_plural = "Приглашения"

    def get_absolute_url(self):
        return reverse("invite", kwargs={"url_uuid": self.pk})

    def __str__(self):
        return "%s" % self.invite_uuid


class UserToCourse(models.Model):
    id = models.BigAutoField(primary_key=True)
    invite_uuid = models.ForeignKey(InviteUrl, on_delete=models.PROTECT, verbose_name="UUID приглашения(ссылки)")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Студент")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс")

    class Meta:
        verbose_name = "Доступ пользователя к курсу"
        verbose_name_plural = "Доступы пользователей к курсам"
