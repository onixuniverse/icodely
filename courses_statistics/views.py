from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView

from courses.mixins import ContextMixin
from courses_statistics.models import UserStatistics


class StudentStatistics(LoginRequiredMixin, ContextMixin, DetailView):
    model = UserStatistics
    template_name = "courses_statistics/student_statistics.html"
    context_object_name = "statistics"

    def get_object(self, queryset=None):
        return UserStatistics.objects.filter(user=self.request.user)


class TutorStatistics(LoginRequiredMixin, ContextMixin, DetailView):
    ...


class CourseStatistics(LoginRequiredMixin, ContextMixin, DetailView):
    model = UserStatistics
    template_name = "courses_statistics/course_statistics.html"
    context_object_name = "statistics"

    def get_object(self, queryset=None):
        return UserStatistics.objects.filter(user=self.request.user)
