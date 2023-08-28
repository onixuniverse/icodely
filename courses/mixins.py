from django.core.exceptions import PermissionDenied


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




class StudentMixin:
    def get_user_context(self, **kwargs):
        pass

