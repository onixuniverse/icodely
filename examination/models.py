from django.db import models
from django.urls import reverse

from courses.models import Lesson, CustomUser


class Examination(models.Model):
    title = models.CharField(max_length=63, verbose_name="Название теста")
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Автор")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name="Урок")

    class Meta:
        verbose_name = "Тестирование"
        verbose_name_plural = "Тестирование"

    def get_absolute_url(self):
        return reverse("exam", kwargs={'exam_id': self.pk})

    def __str__(self):
        return "%s" % self.title


class ExaminationQuestion(models.Model):
    exam = models.ForeignKey(Examination, on_delete=models.CASCADE, verbose_name="Тестирование")
    question = models.TextField(max_length=255, verbose_name="Вопрос")
    question_image = models.ImageField(upload_to="lessons/exams/images", default=None, blank=True, null=True,
                                       verbose_name="Изображение (необязательно)")
    right_answer = models.CharField(max_length=63, verbose_name="Правильный ответ")

    def get_absolute_url(self):
        return reverse("exam_quest", kwargs={'exam_quest_id': self.pk})

    class Meta:
        verbose_name = "Тестовый вопрос"
        verbose_name_plural = "Тестовые вопросы"

    def __str__(self):
        return "%s" % self.question


class ExaminationAnswer(models.Model):
    question = models.ForeignKey(ExaminationQuestion, on_delete=models.CASCADE, verbose_name="Вопрос")
    answer = models.CharField(max_length=63, verbose_name="Ответ")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Пользователь")

    def get_absolute_url(self):
        return reverse("exam_answer", kwargs={'exam_answer_id': self.pk})

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"
