import uuid
from itertools import zip_longest

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView

from courses_statistics.forms import UploadHomeworkFile
from courses_statistics.models import UserStatistics
from .mixins import MenuMixin, UserToCourseAccessMixin
from .models import Course, Lesson, UserToCourse, InviteUrl, Deadlines, Homework

TITLE = "icodely"
TITLE_WITH_DOT = " • " + TITLE


class AllCoursesListView(LoginRequiredMixin, MenuMixin, ListView):
    model = Course
    template_name = "courses/courses_list.html"
    context_object_name = "courses"
    login_url = reverse_lazy("usermanager:login")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Все курсы" + TITLE_WITH_DOT)

        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Course.objects.filter(is_available=True).select_related("author")


class MyCoursesListView(LoginRequiredMixin, MenuMixin, ListView):
    """List of all available courses"""
    model = Course
    template_name = "courses/my_courses.html"
    context_object_name = "courses"
    login_url = reverse_lazy("usermanager:login")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Мои курсы" + TITLE_WITH_DOT)

        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        user_to_courses = UserToCourse.objects.filter(user_id=self.request.user.id)

        available_courses = Course.objects.none()
        for el in user_to_courses:
            available_courses |= Course.objects.filter(id=el.course_id).select_related("author")

        return available_courses


class AboutCourseDetailView(LoginRequiredMixin, MenuMixin, DetailView):
    model = Course
    template_name = "courses/about_course.html"
    context_object_name = "course"
    login_url = reverse_lazy("usermanager:login")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=kwargs['object'].title + TITLE_WITH_DOT)

        return dict(list(context.items()) + list(c_def.items()))

    def get_object(self, query_set=None):
        return Course.objects.get(id=self.kwargs['course_id'])


class CourseDetailView(LoginRequiredMixin, UserToCourseAccessMixin, MenuMixin, DetailView):
    model = Course
    template_name = "courses/course.html"
    context_object_name = "course"
    login_url = reverse_lazy("usermanager:login")

    def get_context_data(self, *, object_list=None, **kwargs):
        lessons = Lesson.objects.filter(course_id=self.kwargs['course_id'])
        lessons_stats_zip = []

        for lesson in lessons:
            try:
                lessons_stats_zip.append((lesson, UserStatistics.objects.get(user=self.request.user, lesson=lesson)))
            except UserStatistics.DoesNotExist:
                lessons_stats_zip.append((lesson, None))

        c_def = self.get_user_context(title=kwargs['object'].title + TITLE_WITH_DOT,
                                      lessons_stats_zip=lessons_stats_zip)

        context = super().get_context_data(**kwargs)
        return dict(list(context.items()) + list(c_def.items()))

    def get_object(self, query_set=None):
        return Course.objects.get(id=self.kwargs['course_id'])


class LessonDetailView(LoginRequiredMixin, UserToCourseAccessMixin, MenuMixin, DetailView):
    model = Lesson
    template_name = "courses/lesson.html"
    context_object_name = "lesson"
    login_url = reverse_lazy("usermanager:login")

    def get_context_data(self, *, object_list=None, **kwargs):
        try:
            user_statistics = UserStatistics.objects.get(user=self.request.user,
                                                         lesson=self.object)

        except UserStatistics.DoesNotExist:
            user_statistics = UserStatistics(user=self.request.user, lesson=self.object)
            user_statistics.save()

        user_statistics.is_lesson_opened = True
        user_statistics.save()

        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=self.object.title + TITLE_WITH_DOT)

        return dict(list(context.items()) + list(c_def.items()))

    def get_object(self, query_set=None):
        return Lesson.objects.get(id=self.kwargs['lesson_id'])


class HomeworkDetailView(LoginRequiredMixin, UserToCourseAccessMixin, MenuMixin, DetailView):
    model = Homework
    template_name = "courses/homework.html"
    context_object_name = "homework"

    def get_context_data(self, *, object_list=None, **kwargs):
        lesson = Lesson.objects.get(id=self.kwargs["lesson_id"])
        try:
            user_statistics = UserStatistics.objects.get(user=self.request.user,
                                                         lesson=lesson)
        except UserStatistics.DoesNotExist:
            user_statistics = UserStatistics(user=self.request.user,
                                             lesson=lesson)
            user_statistics.save()

        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=str(kwargs['object']) + TITLE_WITH_DOT,
                                      statistics=user_statistics,
                                      exam_max_attempts=kwargs["object"].exam.max_attempts,
                                      course_id=lesson.course.id,
                                      lesson=lesson,
                                      form=UploadHomeworkFile(self.request.POST, self.request.FILES))
        return dict(list(context.items()) + list(c_def.items()))

    def post(self, request, *args, **kwargs):
        print(request.POST)

        return redirect("courses:homework", kwargs['course_id'], kwargs["lesson_id"], kwargs["homework_id"])

    def get_object(self, queryset=None):
        return Homework.objects.get(id=self.kwargs["homework_id"])


# Deadlines
class DeadlineListView(LoginRequiredMixin, MenuMixin, ListView):
    model = Deadlines
    template_name = "courses/deadlines.html"


@login_required
def free_course(request, course_id):
    """Create invite and redirect to a free course"""
    course = Course.objects.get(id=course_id)

    try:
        invite = InviteUrl.objects.get(course=course)
    except InviteUrl.DoesNotExist:
        invite = InviteUrl(invite_uuid=uuid.uuid4(), course=course, created_by=request.user)
        invite.save()

    try:
        exist_access_to_course = UserToCourse.objects.get(invite_uuid=invite.pk, user=request.user)
    except UserToCourse.DoesNotExist:
        exist_access_to_course = None

    if not exist_access_to_course:
        new_access_to_course = UserToCourse(invite_uuid=invite, user=request.user, course=course)
        new_access_to_course.save()

    return HttpResponseRedirect(reverse("courses:course", args=[course_id]))


@login_required
def invite_redirect(request):
    """Checks and redirect to course page if access is exist"""
    if request.user.is_authenticated:
        invite = InviteUrl.objects.get(invite_uuid=request.GET["url"])

        if invite:
            try:
                exist_access_to_course = UserToCourse.objects.get(invite_uuid=invite.pk, user=request.user)
            except UserToCourse.DoesNotExist:
                exist_access_to_course = None

            if not exist_access_to_course:
                new_access_to_course = UserToCourse(invite_uuid=invite, user=request.user, course=invite.course)
                new_access_to_course.save()

                return HttpResponseRedirect(reverse("courses:course", args=[invite.course.id]))

        return HttpResponseRedirect(reverse("courses:index"))
    else:
        return HttpResponseRedirect(reverse("usermanager:login"))


def to_courses_page(request):
    """Redirect to courses page"""
    return HttpResponseRedirect(reverse("courses"))


def index_page(request):
    """Render a main page"""
    return render(request, "courses/index.html", {"title": TITLE})


# Errors handler
def page_not_found_404(request, exception):
    context = {
        "title": "404 - Страница не найдена" + TITLE_WITH_DOT
    }
    return render(request, "courses/404.html", context=context, status=404)


def page_internal_error_500(request, exception):
    context = {
        "title": "500 - Ошибка сервера" + TITLE_WITH_DOT
    }

    return render(request, "courses/500.html", context=context, status=500)
