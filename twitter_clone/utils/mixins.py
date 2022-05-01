from django.core.exceptions import ImproperlyConfigured
from braces.views import JSONResponseMixin

from tweets.forms import TweetForm

class DataMixin:
    '''Общий миксин с данными, которые используются на каждой странице (например, форма для твитов).'''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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