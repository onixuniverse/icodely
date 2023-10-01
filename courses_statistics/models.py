from django.db import models

from courses.models import Lesson
from usermanager.models import CustomUser


class UserStatistics(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, verbose_name="Пользователь")
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True, verbose_name="Урок")
    exam_attempts = models.PositiveSmallIntegerField(default=0, blank=True, null=True, verbose_name="Количество попыток")
    exam_result = models.IntegerField(default=0, blank=True, null=True, verbose_name="Результаты теста")
    homework_upload_file = models.FileField(upload_to="uploads/homework/user/", null=True, blank=True,
                                            verbose_name="Файл с Д/З")
    homework_result = models.IntegerField(default=0, blank=True, null=True, verbose_name="Результаты Д/З")
    homework_comment = models.TextField(max_length=255, blank=True, null=True, verbose_name="Комментарий к работе")
    is_exam_complete = models.BooleanField(default=False, verbose_name="Тест решен?")
    is_homework_complete = models.BooleanField(default=False, verbose_name="Д/З сдано?")
    is_homework_checked = models.BooleanField(default=False, verbose_name="Д/З проверено?")
    status = models.CharField(max_length=15, default="Доступно", verbose_name="Статус")  # TODO: remove status

    class Meta:
        verbose_name = "Статистика"
        verbose_name_plural = "Статистики"
