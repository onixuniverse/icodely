from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import DetailView

from courses.mixins import ContextMixin
from courses_statistics.models import UserStatistics
