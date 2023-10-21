from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView

from courses.mixins import ContextMixin
from usermanager.forms import UserRegistrationForm, UserLoginForm, ProfileUpdateForm
from usermanager.models import CustomUser

TITLE = "icodely"
TITLE_WITH_DOT = " • " + TITLE


class RegistrationUser(ContextMixin, CreateView):
    """User registration page"""
    form_class = UserRegistrationForm
    template_name = "usermanager/registration.html"
    success_url = reverse_lazy("usermanager:login")

    def get_user_context(self, object_list=None, **kwargs):
        context = super().get_user_context(**kwargs)
        c_def = self.get_user_context(title="Регистрация" + TITLE_WITH_DOT)

        return dict(list(context.items()) + list(c_def.items()))

    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed

        if request.user.is_authenticated:
            handler = HttpResponseRedirect(reverse_lazy("usermanager:login"))

            return handler

        return handler(request, *args, **kwargs)


class LoginUser(ContextMixin, LoginView):
    """User login page"""
    form_class = UserLoginForm
    template_name = "usermanager/login.html"

    def form_valid(self, form):
        remember_me = form.cleaned_data['remember_me']
        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True

        return super(LoginUser, self).form_valid(form)

    def get_user_context(self, object_list=None, **kwargs):
        context = super().get_user_context(**kwargs)
        c_def = self.get_user_context(title="Авторизация" + TITLE_WITH_DOT)

        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        to = "/"

        if self.request.GET:
            to = self.request.GET["next"] if self.request.GET["next"] != "/logout/" else "/"

        return to

    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() in self.http_method_names and not request.user.is_authenticated:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed

        if request.user.is_authenticated:
            handler = HttpResponseRedirect(reverse_lazy("courses:index"))

            return handler

        return handler(request, *args, **kwargs)


class LogoutUser(LoginRequiredMixin, LogoutView):
    login_url = reverse_lazy("usermanager:login")

    def get_success_url(self):
        return reverse("courses:index")


class ProfileView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = ProfileUpdateForm
    template_name = "usermanager/profile.html"
    login_url = reverse_lazy("usermanager:login")
    success_url = reverse_lazy("usermanager:profile")

    def get_object(self, queryset=None):
        return self.request.user


class ChangeUserPassword(LoginRequiredMixin, UpdateView):
    ...
