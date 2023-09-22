from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView

from courses.mixins import MenuMixin
from courses.models import Homework, Lesson
from examination.forms import ExamAnswerForm
from examination.models import ExaminationQuestion, Examination, ExaminationAnswer

TITLE = "icodely"
TITLE_WITH_DOT = " • " + TITLE


class ExaminationView(LoginRequiredMixin, MenuMixin, DetailView):
    model = Examination
    template_name = "examination/exam.html"
    login_url = reverse_lazy("usermanager:login")

    def get_object(self, query_set=None):
        return Examination.objects.get(id=self.kwargs['exam_id'])


class ExamNewAnswerView(LoginRequiredMixin, MenuMixin, CreateView):
    # form_class = AddExaminationAnswerForm
    template_name = "examination/exam.html"
    login_url = reverse_lazy("usermanager:login")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.request.GET)
        exam = Examination.objects.get(id=2)
        questions = ExaminationQuestion.objects.filter(exam=exam)

        # for q in exam:
        #     questions.append(q)

        c_def = self.get_user_context(title="Добавить урок" + TITLE_WITH_DOT,
                                      question=questions)

        return dict(list(context.items()) + list(c_def.items()))


@login_required
def exam_view(request, exam_id):
    try:
        exam = Examination.objects.get(id=exam_id)
        questions = ExaminationQuestion.objects.filter(exam=exam)
    except Examination.DoesNotExist:
        return HttpResponseRedirect(reverse("courses:index"))  # TODO: 404 redirect

    AnswersFormSet = formset_factory(ExamAnswerForm, extra=len(questions), max_num=len(questions))
    data = {
        "form-TOTAL_FORMS": str(len(questions)),
        "form-INITIAL_FORMS": "0"
    }
    formset = AnswersFormSet(data, prefix="form")
    formset_errors = []

    if request.method == "POST":
        if formset.is_valid():
            answers = [request.POST[f"form-{n}-answer"] for n in range(len(request.POST)-1)]
            for form, question, answer in zip(formset, questions, answers):
                new_answer = form.save(commit=False)
                new_answer.user = request.user
                new_answer.question = question
                new_answer.answer = answer
                new_answer.save()

            homework = Homework.objects.get(exam=exam)
            lesson = Lesson.objects.get(homework=homework)
            redirect_to = reverse("courses:homework", args=[lesson.course.id, lesson.id, homework.id])
            return HttpResponseRedirect(redirect_to)
        else:
            formset_errors = formset.errors

    context = {
        "exam_id": exam_id,
        "formset": formset,
        "ans_quest_array": [(i, j) for i, j in zip(formset, questions)],
        "formset_errors": formset_errors
    }

    return render(request, "examination/exam.html", context=context)
