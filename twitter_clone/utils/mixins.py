from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url
from django.urls import reverse
from django.utils.safestring import mark_safe

from braces.views import JSONResponseMixin

from tweets.forms import TweetForm

class DataMixin:
    '''Общий миксин с данными, которые используются на каждой странице (например, форма для твитов).'''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Количество непрочитынных текущим авторизованным пользователем уведомлений.
        context['unread_notifications'] = user.notifications.filter(usernotification__is_viewed=False). \
                                                exclude(user=user).count()
        context['tweet_form'] = TweetForm()
        return context

class M2MEditMixin(JSONResponseMixin):
    '''Миксин для работы с M2M полями моделей.'''

    field = None
    action = None
    calculate_quantity = False
    response_dict = {}
    error_message = 'При выполнении текущего запроса произошла ошибка.'

    def post(self, request, *args, **kwargs):
        if self.calculate_quantity:
            quantity = self.get_quantity()
            self.response_dict.update(quantity=quantity)
        return self.render_json_response(self.response_dict, status=200)

    def get_model_field(self, obj):
        '''Возвращает атрибут экземпляра класса модели, если он существует.'''
        if self.field is None:
            raise ImproperlyConfigured(
                "Значение атрибута 'field' не найдено."
            )
        attr = getattr(obj, self.field, None)
        if attr is None:
            raise ImproperlyConfigured(
                f"Атрибут '{attr}' модели не найден. Укажите корректный атрибут."
            )
        return attr

    def get_action(self):
        '''Возвращает действие для работы с экземляром класса, если оно существует и корректо.'''
        if self.action is None:
            raise ImproperlyConfigured(
                "Значение атрибута 'action' не найдено."
            )
        if self.action not in ('add', 'remove'):
            raise ImproperlyConfigured(
                "Значение атрибута 'action' должно быть или 'add', или 'remove'."
            )
        return self.action

    def get_quantity(self):
        '''Возвращает количество пользователей для найденного атрибута экземпляра класса модели.'''
        return self.model_field.count()

class SimpleLoginRequiredMixin(AccessMixin):
    '''
    Проверяет, авторизован ли пользователь.
    Если нет - перенаправляет на страницу логина без "next" параметра.
    '''

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            resolved_login_url = resolve_url(self.get_login_url())
            return HttpResponseRedirect(resolved_login_url)
        return super().dispatch(request, *args, **kwargs)

class SimpleLoginRequiredAjaxMixin(AccessMixin):
    '''
    Проверяет, авторизован ли пользователь. Если нет - отправляет ответ в формате JSON 
    с соответствующей ошибкой и данными.
    '''

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            resolved_login_url = resolve_url(self.get_login_url())
            return self.render_json_response(
                {
                    'error': 'Неавторизованный пользователь',
                    'login_url': resolved_login_url
                }, 
                status=401
            )
        return super().dispatch(request, *args, **kwargs)

class AdminMixin:
    '''Миксин для работы с классами админ-панели.'''

    @staticmethod
    def get_objects(queryset, line_by_line=False):
        '''
        Возвращает строку с ссылками на объекты из qs в админ панели.

            params:
                    queryset (QuerySet): список объектов
                    line_by_line (Boolean): если True, то выводит объекты построчно,
                                            если False - через запятую.

            return value:
                    строка (str): строка с объектами, являющиеся ссылками
        '''
        object_list = []
        for obj in queryset:
            url = reverse(f'admin:{obj._meta.app_label}_{obj._meta.model_name}_change', args=(obj.pk,))
            if line_by_line:
                object_list.append(f'<p><a href="{url}">{obj}</a></p>')
            else:
                object_list.append(f'<a href="{url}">{obj}</a>')
        if line_by_line:
            return mark_safe(''.join(object_list))
        return mark_safe(', '.join(object_list))