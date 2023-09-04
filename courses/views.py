from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, CreateView, DetailView

from .forms import AddCourseForm, AddLessonForm
from .models import Course, Lesson, UserToCourse, InviteUrl
from .mixins import MenuMixin, GroupRequiredMixin, UserToCourseAccessMixin

TITLE = "icodely"
TITLE_WITH_DOT = " • " + TITLE


def to_courses_page(request):
    """Redirect to /courses/"""
    return HttpResponseRedirect(reverse("courses"))


# Index page
def index_page(request):
    return render(request, "courses/index.html", {"title": TITLE})


# Course & Lessons View
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


class TeachersCourses(LoginRequiredMixin, GroupRequiredMixin, MenuMixin, ListView):
    model = Course
    template_name = "courses/old_courses_list.html.html"
    context_object_name = "courses"
    login_url = reverse_lazy("usermanager:login")
    group_required = [u'teacher']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Мои курсы (учитель)")

        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        available_courses = Course.objects.filter(author_id=self.request.user.id)

        return available_courses


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


class CourseLessonsDetailView(LoginRequiredMixin, UserToCourseAccessMixin, MenuMixin, DetailView):
    """Page of the selected course"""
    model = Course
    template_name = "courses/course.html"
    context_object_name = "course"
    login_url = reverse_lazy("usermanager:login")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=kwargs['object'].title + TITLE_WITH_DOT,
                                      lessons=Lesson.objects.filter(course_id=self.kwargs['course_id']),
                                      lesson_status="N/A")

        return dict(list(context.items()) + list(c_def.items()))

    def get_object(self, query_set=None):
        return Course.objects.get(id=self.kwargs['course_id'])


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


class ShowLesson(LoginRequiredMixin, UserToCourseAccessMixin, MenuMixin, DetailView):
    """Page of the selected lesson in the course"""
    model = Lesson
    template_name = "courses/lesson.html"
    context_object_name = "lesson"
    login_url = reverse_lazy("usermanager:login")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=kwargs['object'].title + TITLE_WITH_DOT)

        return dict(list(context.items()) + list(c_def.items()))

    def get_object(self, query_set=None):
        return Lesson.objects.get(id=self.kwargs['lesson_id'])


# Add new Courses & Lessons
class AddCourse(LoginRequiredMixin, GroupRequiredMixin, MenuMixin, CreateView):
    """Page form with adding a new course"""
    form_class = AddCourseForm
    template_name = "courses/add_course.html"
    login_url = reverse_lazy("usermanager:login")
    group_required = [u"teacher"]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавить курс" + TITLE_WITH_DOT)

        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        self.obj = form.save(commit=False)
        self.obj.author = self.request.user
        self.obj.save()

        return super().form_valid(form)


class AddLesson(LoginRequiredMixin, GroupRequiredMixin, MenuMixin, CreateView):
    """Page of adding a new lesson in a course"""
    form_class = AddLessonForm
    template_name = "courses/add_lesson.html"
    login_url = reverse_lazy("usermanager:login")
    group_required = [u"teacher"]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавить урок" + TITLE_WITH_DOT)

        return dict(list(context.items()) + list(c_def.items()))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user

        return kwargs


# Deadlines
class DeadlineView(View):
    pass


# Invite links handlers
class InviteView(LoginRequiredMixin, View):
    model = InviteUrl

    def get_success_url(self):
        to = "/"

        if self.request.GET:
            to = self.request.GET["url"]

        return to


def invite_redirect(request):
    invite = InviteUrl.objects.get(invite_uuid=request.GET["url"])

    if invite:
        try:
            exist_access_to_course = UserToCourse.objects.get(invite_uuid=invite.pk, user=request.user)
        except:
            exist_access_to_course = None

        if not exist_access_to_course:
            new_access_to_course = UserToCourse(invite_uuid=invite, user=request.user, course=invite.course)
            new_access_to_course.save()

            return HttpResponseRedirect(reverse("courses:course", args=[invite.course.id]))

    return HttpResponseRedirect(reverse("courses:index"))


# Errors handler
def page_not_found_404(request, exception):
    context = {
        "title": "Страница не найдена" + TITLE_WITH_DOT
    }
    return render(request, "courses/404.html", context=context, status=404)


