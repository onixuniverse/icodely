from django.db import models

from courses.models import Lesson
from usermanager.models import CustomUser


class UserStatistics(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, verbose_name="Пользователь (не менять)")
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True, verbose_name="Урок (не менять)")
    exam_attempts = models.PositiveSmallIntegerField(default=0, blank=True, null=True,
                                                     verbose_name="Количество попыток (не менять)")
    exam_result = models.IntegerField(default=0, blank=True, null=True, verbose_name="Результаты теста (не менять)")
    homework_upload_file = models.FileField(upload_to="uploads/homework/user/", null=True, blank=True,
                                            verbose_name="Файл с Д/З (не менять)")
    homework_result = models.IntegerField(default=0, blank=True, null=True, verbose_name="Результаты Д/З")
    homework_comment = models.TextField(max_length=255, blank=True, null=True, verbose_name="Комментарий к работе")
    is_exam_complete = models.BooleanField(default=False, verbose_name="Тест решен? (не менять)")
    is_homework_complete = models.BooleanField(default=False, verbose_name="Д/З сдано? (не менять)")
    is_homework_checked = models.BooleanField(default=False, verbose_name="Д/З проверено?")
    is_lesson_opened = models.BooleanField(default=False, verbose_name="Урок был открыт? (не менять)")
    status = models.CharField(max_length=15, default="Доступно", verbose_name="Статус")

    class Meta:
        verbose_name = "Статистика"
        verbose_name_plural = "Статистики"
