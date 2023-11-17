import uuid

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, UpdateView

from courses_statistics.forms import UploadHomeworkFile
from courses_statistics.models import UserStatistics
from examination.models import ExaminationQuestion
from .mixins import ContextMixin, UserToCourseAccessMixin
from .models import Course, Lesson, UserToCourse, InviteUrl, Deadlines, Homework

TITLE = "icodely"
TITLE_WITH_DOT = " • " + TITLE


class AllCoursesListView(LoginRequiredMixin, ContextMixin, ListView):
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


class MyCoursesListView(LoginRequiredMixin, ContextMixin, ListView):
    model = Course
    template_name = "courses/my_courses.html"
    context_object_name = "courses"
    login_url = reverse_lazy("usermanager:login")

    def get_context_data(self, *, object_list=None, **kwargs):
        course_progress = []
        for obj in self.object_list:
            lessons_by_course = Lesson.objects.filter(course=obj)
            user_course_stat = UserStatistics.objects.filter(user=self.request.user, lesson__in=lessons_by_course)
            passed_lessons = 0
            for el in user_course_stat:
                if el.is_complete:
                    passed_lessons += 1

            course_progress.append((round((passed_lessons / len(lessons_by_course)) * 100)) if passed_lessons != 0 else 0)

        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Мои курсы" + TITLE_WITH_DOT,
                                      courses_progress=zip(self.object_list, course_progress))

        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        user_to_courses = UserToCourse.objects.filter(user_id=self.request.user.id)

        available_courses = Course.objects.none()
        for el in user_to_courses:
            available_courses |= Course.objects.filter(id=el.course_id).select_related("author")

        return available_courses


class AboutCourseDetailView(LoginRequiredMixin, ContextMixin, DetailView):
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


class CourseDetailView(LoginRequiredMixin, UserToCourseAccessMixin, ContextMixin, DetailView):
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


class LessonDetailView(LoginRequiredMixin, UserToCourseAccessMixin, ContextMixin, DetailView):
    model = Lesson
    template_name = "courses/lesson.html"
    context_object_name = "lesson"
    login_url = reverse_lazy("usermanager:login")

    def get_context_data(self, *, object_list=None, **kwargs):
        try:
            user_statistics = UserStatistics.objects.get(user=self.request.user, lesson=self.object)

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


class HomeworkDetailView(LoginRequiredMixin, UserToCourseAccessMixin, ContextMixin, UpdateView):
    model = Homework
    form_class = UploadHomeworkFile
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
        c_def = self.get_user_context(title=str(self.object.title) + TITLE_WITH_DOT,
                                      statistics=user_statistics,
                                      exam=self.object.exam,
                                      exam_max_result=len(ExaminationQuestion.objects.filter(exam=self.object.exam)),
                                      course_id=lesson.course.id,
                                      lesson=lesson)
        return dict(list(context.items()) + list(c_def.items()))

    def post(self, request, *args, **kwargs):
        return super(HomeworkDetailView, self).post(request, **kwargs)

    def get_object(self, queryset=None):
        return Homework.objects.get(id=self.kwargs["homework_id"])


# Deadlines
class DeadlineListView(LoginRequiredMixin, ContextMixin, ListView):
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
    invite = InviteUrl.objects.get(invite_uuid=request.GET["url"])

    if not invite:
        raise Http404

    try:
        exist_access_to_course = UserToCourse.objects.get(invite_uuid=invite.pk, user=request.user)
    except UserToCourse.DoesNotExist:
        exist_access_to_course = None

    if not exist_access_to_course:
        new_access_to_course = UserToCourse(invite_uuid=invite, user=request.user, course=invite.course)
        new_access_to_course.save()

        return HttpResponseRedirect(reverse("courses:course", args=[invite.course.id]))


# Errors handler
def page_forbidden_403(request, exception):
    context = {
        "title": "Доступ запрещен" + TITLE_WITH_DOT,
        "content": "Доступ запрещен"
    }

    return render(request, "courses/http_error.html", context=context, status=403)


def page_not_found_404(request, exception):
    context = {
        "title": "Страница не найден" + TITLE_WITH_DOT,
        "content": "Страница не найдена"
    }

    return render(request, "courses/http_error.html", context=context, status=404)


def page_method_not_allow_405(request, exception):
    context = {
        "title": "Метод не разрешен" + TITLE_WITH_DOT,
        "content": "Метод не разрешен"
    }

    return render(request, "courses/http_error.html", context=context, status=405)


def page_internal_error_500(request):
    context = {
        "title": "Внутренняя ошибка сервера" + TITLE_WITH_DOT,
        "content": "Внутренняя ошибка сервера"
    }

    return render(request, "courses/http_error.html", context=context, status=500)
