import uuid

from django.db import models
from django.urls import reverse

from examination.models import Examination
from usermanager.models import CustomUser


class Course(models.Model):
    title = models.CharField(max_length=63, verbose_name="Название курса")
    short_description = models.CharField(max_length=53, blank=True, null=True, verbose_name="Краткое описание")
    description = models.TextField(max_length=1023, verbose_name="Описание курса", blank=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Автор курса")
    is_available = models.BooleanField(default=True, verbose_name="Курс доступен сразу?")
    steps = models.PositiveSmallIntegerField(default=0, verbose_name="Количество шагов")
    is_free = models.BooleanField(default=False, verbose_name="Бесплатный курс?")
    full_price = models.PositiveIntegerField(default=0, verbose_name="Цена за весь курс")
    month_price = models.PositiveSmallIntegerField(default=0, blank=True, null=True,
                                                   verbose_name="Цена в месяц за курс")
    course_duration = models.PositiveSmallIntegerField(default=0, verbose_name="Длительность курса (в мес.)")

    backplate_color_choices = [
        ("gray", "Серый"),
        ("yellow", "Желтый"),
        ("pink", "Розовый"),
        ("blue", "Голубой")
    ]
    backplate_color = models.CharField(max_length=6, default="gray", choices=backplate_color_choices,
                                       verbose_name="Цвет подкладки")

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def get_absolute_url(self):
        return reverse("courses:course", kwargs={'course_id': self.pk})

    def __str__(self):
        return "%s" % self.title

    def save(self, *args, **kwargs):
        self.is_free = False if self.full_price else True
        self.steps = len(Lesson.objects.filter(course=self))

        super().save(*args, **kwargs)


class Homework(models.Model):
    title = models.CharField(max_length=63, verbose_name="Название Д/З")
    description = models.TextField(max_length=255, verbose_name="Описание")
    homework_file = models.FileField(upload_to="uploads/homework/files/", default=None, null=True, blank=True,
                                     verbose_name="Файл с Д/З")
    homework_max_result = models.IntegerField(default=10, verbose_name="Максимальный балл за файл с Д/З")
    homework_url = models.CharField(max_length=127, null=True, blank=True, verbose_name="Ссылка на Д/З")
    exam = models.OneToOneField(Examination, on_delete=models.PROTECT, null=True, blank=True,
                                verbose_name="Тестирование")

    class Meta:
        verbose_name = "Домашняя работа"
        verbose_name_plural = "Домашние работы"

    def get_absolute_url(self):
        return reverse("courses:homework", kwargs={'homework_id': self.pk, "lesson_id": self.lesson.id,
                                                   "course_id": self.lesson.course.id})

    def __str__(self):
        return "%s" % self.title


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.PROTECT, verbose_name="Курс")
    title = models.CharField(max_length=57, verbose_name="Название урока")
    short_description = models.TextField(max_length=63, verbose_name="Краткое описание урока")
    content = models.TextField(max_length=4095, verbose_name="Содержание урока")
    homework = models.OneToOneField(Homework, on_delete=models.PROTECT, default=None, blank=True, null=True,
                                    verbose_name="Д/З")
    video_youtube = models.CharField(max_length=127, default=None, blank=True, null=True,
                                     verbose_name="EMBED-ссылка на видео с Youtube")
    pdf_file = models.FileField(upload_to="uploads/lessons/pdf/", default=None, null=True, blank=True,
                                verbose_name="PDF-файл")

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def get_absolute_url(self):
        return reverse("courses:lesson", kwargs={'lesson_id': self.pk, 'course_id': self.course.id})

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
        return reverse("courses:invite", kwargs={"url_uuid": self.pk})

    def __str__(self):
        return "%s" % self.invite_uuid


class Deadlines(models.Model):
    pass


class UserToCourse(models.Model):
    id = models.BigAutoField(primary_key=True)
    invite_uuid = models.ForeignKey(InviteUrl, on_delete=models.PROTECT, editable=False,
                                    verbose_name="UUID приглашения(ссылки)")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, editable=False, verbose_name="Студент")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, editable=False, verbose_name="Курс")

    class Meta:
        verbose_name = "Доступ пользователя к курсу"
        verbose_name_plural = "Доступы пользователей к курсам"
