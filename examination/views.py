from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.forms import formset_factory
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, ListView

from courses.forms import WrongAnswerByUserForm
from courses.mixins import MenuMixin
from courses.models import Homework, Lesson, Course
from courses_statistics.models import UserStatistics
from examination.forms import ExamAnswerForm
from examination.models import ExaminationQuestion, Examination, ExaminationAnswer

TITLE = "icodely"
TITLE_WITH_DOT = " • " + TITLE


@login_required
def exam_view(request, exam_id):
    try:
        exam = Examination.objects.get(id=exam_id)
        questions = ExaminationQuestion.objects.filter(exam=exam)
    except Examination.DoesNotExist:
        return HttpResponseRedirect(reverse("courses:index"))  # TODO: 404 redirect

    homework = Homework.objects.get(exam=exam)
    lesson = Lesson.objects.get(homework=homework)
    try:
        user_statistics = UserStatistics.objects.get(user=request.user, lesson=lesson)
    except UserStatistics.DoesNotExist:
        user_statistics = UserStatistics(user=request.user, lesson=lesson)
        user_statistics.save()

    if user_statistics.exam_attempts >= exam.max_attempts:
        return HttpResponseForbidden()

    AnswersFormSet = formset_factory(ExamAnswerForm, extra=len(questions), max_num=len(questions))
    data = {
        "form-TOTAL_FORMS": str(len(questions)),
        "form-INITIAL_FORMS": "0"
    }
    formset = AnswersFormSet(data, prefix="form")
    formset_errors = []

    if request.method == "POST":
        if formset.is_valid():
            answers = [request.POST[f"form-{n}-answer"] for n in range(len(request.POST) - 1)]
            amount_right_answers = 0
            for form, question, answer in zip(formset, questions, answers):
                try:
                    new_answer = ExaminationAnswer.objects.get(user=request.user, question=question)
                except ExaminationAnswer.DoesNotExist:
                    new_answer = form.save(commit=False)
                    new_answer.user = request.user
                    new_answer.question = question

                new_answer.answer = answer

                if answer == question.right_answer:
                    new_answer.is_answer_right = 1
                    amount_right_answers += 1
                else:
                    new_answer.is_answer_right = 0
                new_answer.save()

            user_statistics.exam_result = amount_right_answers
            user_statistics.exam_attempts += 1
            user_statistics.is_exam_complete = True
            user_statistics.save()

            redirect_to = reverse("examination:exam_result", args=[exam_id])
            return HttpResponseRedirect(redirect_to)
        else:
            formset_errors = formset.errors

    context = {
        "exam_id": exam_id,
        "exam_title": exam.title,
        "formset": formset,
        "ans_quest_array": [(i, j) for i, j in zip(formset, questions)],
        "formset_errors": formset_errors
    }

    return render(request, "examination/exam.html", context=context)


class ExamResultView(LoginRequiredMixin, MenuMixin, DetailView):
    model = UserStatistics
    template_name = "examination/exam_result.html"
    context_object_name = "statistics"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        exam = Examination.objects.get(id=self.kwargs["exam_id"])
        c_def = self.get_user_context(title="Результаты теста" + TITLE_WITH_DOT,
                                      exam_max_attempts=exam.max_attempts,
                                      exam_max_result=len(ExaminationQuestion.objects.filter(exam=exam)))

        return dict(list(context.items()) + list(c_def.items()))

    def get_object(self, queryset=None):
        return UserStatistics.objects.get(user=self.request.user, lesson=Lesson.objects.get(
            homework=Homework.objects.get(exam=Examination.objects.get(id=self.kwargs["exam_id"]))))


def wrong_answer_view(request):
    if request.user.is_staff:
        form = WrongAnswerByUserForm(request.POST or None)
        wrong_answers = []
        if request.POST and form.is_valid():
            user = form.cleaned_data["user"]

            wrong_answers = ExaminationAnswer.objects.filter(user=user, is_answer_right=0)

        context = {
            "form": form,
            "wrong_answers": wrong_answers
        }

        return render(request, "examination/wrong_answers.html", context=context)


