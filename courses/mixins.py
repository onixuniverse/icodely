from django.core.exceptions import PermissionDenied

from courses.models import UserToCourse, Homework, Lesson
from examination.models import Examination

menu = [{'text': 'Главная', 'url_name': 'index'},
        {'text': 'Добавить курс', 'url_name': 'addcourse'},
        {'text': 'Войти', 'url_name': 'login'},
        {'text': 'Регистрация', 'url_name': 'register'},
        {'text': 'Выйти', 'url_name': 'logout'}]


class MenuMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        user_menu = menu.copy()
        # if not self.request.user.is_authenticated:
        #     user_menu.pop(1)
        #     user_menu.pop(3)
        # else:
        #     user_menu.pop(2)
        #     user_menu.pop(2)

        context['menu'] = user_menu

        return context


class GroupRequiredMixin:
    """
        group_required - list of strings, required param

        from: https://gist.github.com/ceolson01/206139a093b3617155a6
    """

    group_required = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied
        else:
            user_groups = []
            for group in request.user.groups.values_list('name', flat=True):
                user_groups.append(group)
            if len(set(user_groups).intersection(self.group_required)) <= 0:
                raise PermissionDenied
        return super(GroupRequiredMixin, self).dispatch(request, *args, **kwargs)


def course_access(func):
    def decorator(request, *args, **kwargs):
        if "course_id" in kwargs.keys():
            user_to_course_access = UserToCourse.objects.filter(user=request.user, course_id=kwargs['course_id'])
        elif "exam_id" in kwargs.keys():
            user_to_course_access = UserToCourse.objects.filter(user=request.user,
                                                                course=Lesson.objects.get(homework=Homework.objects.get(
                                                                    exam=Examination.objects.get(
                                                                        id=kwargs["exam_id"]))).course)

        if not user_to_course_access:
            raise PermissionDenied

    return decorator


class UserToCourseAccessMixin:
    def dispatch(self, request, *args, **kwargs):
        if "course_id" in kwargs.keys():
            user_to_course_access = UserToCourse.objects.filter(user=request.user, course_id=kwargs['course_id'])
        elif "exam_id" in kwargs.keys():
            user_to_course_access = UserToCourse.objects.filter(user=request.user,
                                                                course=Lesson.objects.get(homework=Homework.objects.get(
                                                                    exam=Examination.objects.get(
                                                                        id=kwargs["exam_id"]))).course)

        if not user_to_course_access:
            raise PermissionDenied

        return super(UserToCourseAccessMixin, self).dispatch(request, *args, **kwargs)
