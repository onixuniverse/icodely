from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory
from django.http import HttpResponseRedirect, HttpResponseForbidden, Http404
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import DetailView

from courses.mixins import ContextMixin, UserToCourseAccessMixin, course_access
from courses.models import Homework, Lesson
from courses_statistics.models import UserStatistics
from examination.forms import ExamAnswerForm, WrongAnswerByUserForm
from examination.models import ExaminationQuestion, Examination, ExaminationAnswer

TITLE = "icodely"
TITLE_WITH_DOT = " • " + TITLE


@login_required
@course_access
def exam_view(request, exam_id):
    try:
        exam = Examination.objects.get(id=exam_id)
        questions = ExaminationQuestion.objects.filter(exam=exam)
    except Examination.DoesNotExist:
        raise Http404

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

                new_answer.answer = answer.lower()

                if answer.lower() == question.right_answer.lower():
                    new_answer.is_answer_right = 1
                    amount_right_answers += 1
                else:
                    new_answer.is_answer_right = 0
                new_answer.save()

            user_statistics.exam_result = amount_right_answers
            user_statistics.exam_attempts += 1
            user_statistics.is_exam_complete = True
            user_statistics.save()

            return HttpResponseRedirect(reverse("examination:exam_result", args=[exam_id]))
        else:
            formset_errors = formset.errors

    context = {
        "title": exam.title + TITLE_WITH_DOT,
        "exam_id": exam_id,
        "exam_title": exam.title,
        "formset": formset,
        "ans_quest_array": [(i, j) for i, j in zip(formset, questions)],
        "formset_errors": formset_errors
    }

    return render(request, "examination/exam.html", context=context)


class ExamResultView(LoginRequiredMixin, UserToCourseAccessMixin, ContextMixin, DetailView):
    model = UserStatistics
    template_name = "examination/exam_result.html"
    context_object_name = "statistics"

    def __init__(self, *kwargs):
        self.exam = None
        super().__init__()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Результаты теста" + TITLE_WITH_DOT,
                                      exam=self.exam,
                                      exam_max_result=len(ExaminationQuestion.objects.filter(exam=self.exam)),
                                      lesson=self.object.lesson,
                                      homework=self.object.lesson.homework)

        return dict(list(context.items()) + list(c_def.items()))

    def get_object(self, queryset=None):
        self.exam = Examination.objects.get(id=self.kwargs["exam_id"])
        return UserStatistics.objects.get(user=self.request.user,
                                          lesson=Lesson.objects.get(homework=Homework.objects.get(exam=self.exam)))


@login_required
def wrong_answer_view(request):
    if request.user.is_staff:
        form = WrongAnswerByUserForm(request.POST or None)
        wrong_answers = []
        if request.POST and form.is_valid():
            user = form.cleaned_data["user"]
            exam = form.cleaned_data["exam"]

            questions = ExaminationQuestion.objects.filter(exam=exam)
            wrong_answers = ExaminationAnswer.objects.filter(question__in=questions, user=user)

        context = {
            "form": form,
            "wrong_answers": wrong_answers
        }

        return render(request, "examination/wrong_answers.html", context=context)
