from django.core.validators import MaxValueValidator
from django.db import models
from django.urls import reverse

from usermanager.models import CustomUser


class Examination(models.Model):
    title = models.CharField(max_length=63, verbose_name="Название теста")
    max_attempts = models.PositiveSmallIntegerField(default=1, verbose_name="Количество попыток",
                                                    validators=[
                                                        MaxValueValidator(limit_value=10,
                                                                          message="Максимальное количество попыток: 10")
                                                    ])

    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Автор")

    class Meta:
        verbose_name = "Тестирование"
        verbose_name_plural = "Тестирование"

    def get_absolute_url(self):
        return reverse("exam", kwargs={'exam_id': self.pk})

    def __str__(self):
        return "%s" % self.title


class ExaminationQuestion(models.Model):
    exam = models.ForeignKey(Examination, on_delete=models.CASCADE, verbose_name="Тестирование")
    question = models.TextField(max_length=1023, verbose_name="Вопрос")
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
    answer = models.CharField(max_length=63, blank=True, null=True, verbose_name="Ответ")
    is_answer_right = models.BooleanField(default=False, verbose_name="Правильный ответ?")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Пользователь")

    def get_absolute_url(self):
        return reverse("exam_quest", kwargs={'exam_id': self.question.exam.id,
                                             'exam_quest_id': self.question.id, 'exam_answer_id': self.pk})

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"
