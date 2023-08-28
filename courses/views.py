from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, CreateView, DetailView

from .forms import AddCourseForm, AddLessonForm, RegistrationUserForm, LoginUserForm
from .models import Course, Lesson, UserToCourse
from .mixins import MenuMixin, GroupRequiredMixin


TITLE = "icodely"
TITLE_WITH_DOT = " • icodely"


def to_courses_page(request):
    """Redirect to /courses/"""
    return HttpResponseRedirect(reverse("courses"))


# Index page
def index_page(request):
    return render(request, "courses/index.html")


# Account
class RegistrationUser(MenuMixin, CreateView):
    """User registration page"""
    form_class = RegistrationUserForm
    template_name = "courses/registration.html"
    success_url = reverse_lazy("login")

    def get_user_context(self, object_list=None, **kwargs):
        context = super().get_user_context(**kwargs)
        c_def = self.get_user_context(title="Регистрация")

        return dict(list(context.items()) + list(c_def.items()))

    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed

        if request.user.is_authenticated:
            handler = HttpResponseRedirect(reverse_lazy("login"))

            return handler

        return handler(request, *args, **kwargs)


class LoginUser(MenuMixin, LoginView):
    """User login page"""
    form_class = LoginUserForm
    template_name = "courses/login.html"

    def form_valid(self, form):
        remember_me = form.cleaned_data['remember_me']
        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True

        return super(LoginUser, self).form_valid(form)

    def get_user_context(self, object_list=None, **kwargs):
        context = super().get_user_context(**kwargs)
        c_def = self.get_user_context(title="Авторизация")

        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        to = "/"

        if self.request.GET:
            to = self.request.GET['next']

        return to

    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() in self.http_method_names and not request.user.is_authenticated:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed

        if request.user.is_authenticated:
            handler = HttpResponseRedirect(reverse_lazy("index"))

            return handler

        return handler(request, *args, **kwargs)


class LogoutUser(LoginRequiredMixin, LogoutView):
    login_url = reverse_lazy("login")

    def get_success_url(self):
        return reverse("index")


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "courses/account.html"
    context_object_name = "user"
    login_url = reverse_lazy("login")

    def get_object(self, queryset=None):
        return User.objects.get(pk=self.request.user.id)


# Course & Lessons View
class MyCourses(LoginRequiredMixin, MenuMixin, ListView):
    """List of all available courses"""
    model = Course
    template_name = "courses/my_courses.html"
    context_object_name = "courses"
    login_url = reverse_lazy("login")

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
    login_url = reverse_lazy("login")
    group_required = [u'teacher']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Мои курсы (учитель)")

        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        available_courses = Course.objects.filter(author_id=self.request.user.id)

        return available_courses


class AllCourses(LoginRequiredMixin, MenuMixin, ListView):
    model = Course
    template_name = "courses/courses_list.html"
    context_object_name = "courses"
    login_url = reverse_lazy("login")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Все курсы" + TITLE_WITH_DOT)

        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Course.objects.filter(is_available=True).select_related("author")


class ShowCourse(LoginRequiredMixin, MenuMixin, DetailView):
    """Page of the selected course"""
    model = Course
    template_name = "courses/course.html"
    context_object_name = "course"
    login_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=Course.title,
                                      lessons=Lesson.objects.filter(course_id=self.kwargs['course_id']),
                                      lesson_status="Выполнено TEST")

        return dict(list(context.items()) + list(c_def.items()))

    def get_object(self, query_set=None):
        return Course.objects.get(id=self.kwargs['course_id'])


class ShowLesson(LoginRequiredMixin, MenuMixin, DetailView):
    """Page of the selected lesson in the course"""
    model = Lesson
    template_name = "courses/lesson.html"
    context_object_name = "lesson"
    login_url = reverse_lazy("login")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()

        return dict(list(context.items()) + list(c_def.items()))

    def get_object(self, query_set=None):
        return Lesson.objects.get(id=self.kwargs['lesson_id'])


# Add new Courses & Lessons
class AddCourse(LoginRequiredMixin, GroupRequiredMixin, MenuMixin, CreateView):
    """Page form with adding a new course"""
    form_class = AddCourseForm
    template_name = "courses/add_course.html"
    login_url = reverse_lazy('login')
    group_required = [u"teacher"]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавить курс")

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
    login_url = reverse_lazy('login')
    group_required = [u"teacher"]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавить урок")

        return dict(list(context.items()) + list(c_def.items()))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user

        return kwargs


# Deadlines
class DeadlineView(View):
    pass


# Invite links handlers
class CrateNewInviteLink(LoginRequiredMixin, GroupRequiredMixin, MenuMixin, CreateView):
    pass


# Error handler
def page_not_found_404(request, exception):
    return HttpResponseNotFound("<h1>404</h1><h2>Page not found!</h2>")
