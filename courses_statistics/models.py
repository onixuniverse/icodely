from django.db import models
from django.urls import reverse

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
    is_homework = models.BooleanField(default=False, verbose_name="Имеет Д/З? (не менять)")
    is_written_homework = models.BooleanField(default=False, verbose_name="Имеет письменную Д/З? (не менять)")
    is_homework_has_exam = models.BooleanField(default=False, verbose_name="Имеет тест в Д/З? (не менять)")
    is_exam_complete = models.BooleanField(default=False, verbose_name="Тест решен? (не менять)")
    is_homework_complete = models.BooleanField(default=False, verbose_name="Д/З сдано? (не менять)")
    is_homework_checked = models.BooleanField(default=False, verbose_name="Д/З проверено?")
    is_lesson_opened = models.BooleanField(default=False, verbose_name="Урок был открыт? (не менять)")
    last_time_lesson_opened = models.DateTimeField(auto_now=True, verbose_name="Последний заход на урок (не менять)")
    status = models.CharField(max_length=15, default="Доступен", verbose_name="Статус")
    is_complete = models.BooleanField(default=False, verbose_name="Выполнено? (не менять)")

    def save(self, *args, **kwargs):
        if self.lesson.homework:
            self.is_homework = True
            if self.lesson.homework.exam:
                self.is_homework_has_exam = True
            if self.lesson.homework.homework_file:
                self.is_written_homework = True

        if self.is_lesson_opened or self.is_homework_complete or self.is_exam_complete:
            self.status = "Выполняется"

            if not self.is_homework and self.is_lesson_opened:
                self.is_complete = True

        if self.is_written_homework:
            if self.is_homework_complete:
                self.status = "Задание на проверке"
            if self.is_homework_checked:
                self.status = "Задание выполнено"

        if (((self.is_homework_has_exam and self.is_exam_complete) and (self.is_written_homework and self.is_homework_checked)) or
                (not self.is_homework_has_exam and (self.is_written_homework and self.is_homework_checked)) or
                ((self.is_homework_has_exam and self.is_exam_complete) and not self.is_written_homework)):
            self.is_complete = True

        if self.is_complete:
            self.status = "Выполнено"

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("courses_statistics:user_stats", kwargs={'statistics_id': self.pk})

    class Meta:
        verbose_name = "Статистика"
        verbose_name_plural = "Статистика"
