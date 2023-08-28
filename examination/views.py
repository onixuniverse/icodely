from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import modelformset_factory
from django.shortcuts import render

from examination.models import ExaminationAnswer, ExaminationQuestion


def exam_view(request):

    # creating a formset
    ExaminationFormSet = modelformset_factory(ExaminationAnswer, fields=["question", "answer"])
    formset = ExaminationFormSet()

    # Add the formset to context dictionary
    context = {
        "formset": formset,
        "questions": ExaminationQuestion.objects.filter()
    }
    return render(request, "examination/exam.html", context)
