import json
from django.core.exceptions import ImproperlyConfigured
from braces.views import JSONResponseMixin
from tweets.models import Tweet

class TweetEditMixin(JSONResponseMixin):
    '''
    Миксин для работы с M2M полями модели Tweet (likes, retweets, bookmarks).
    Получает id твита от клиента и добавляет/удаляет текущего пользователя у найденного экземпляра класса для указанного атрибута и
    отправляет соответствуютщий ответ клиенту в формате json.
    '''

    field = None
    action = None
    calculate_quantity = False
    response_dict = {}
    error_message = 'При выполнении текущего запроса произошла ошибка.'

    def post(self, request, *args, **kwargs):
        '''
        Обрабатывает POST запрос, совершает необходимые действия с экземпляром класса
        и возвращает ответ в формате json.
        '''
        tweet_id = json.load(self.request)['tweet_id']

        # Проверяем, существует ли объект с таким id.
        # Если нет, то выкидываем ошибку и возвращаем ответ.
        try:
            tweet = Tweet.objects.get(pk=tweet_id)
        except Tweet.DoesNotExist:
            self.response_dict.update(error=self.error_message)
            return self.render_json_response(self.response_dict, status=500)

        self.model_field = self.get_model_field(tweet)
        action = self.get_action()
        if action == 'add':
            self.model_field.add(self.request.user)
            self.response_dict.update(result='added')
        if action == 'remove':
            self.model_field.remove(self.request.user)
            self.response_dict.update(result='deleted')
        if self.calculate_quantity:
            quantity = self.get_quantity()
            self.response_dict.update(quantity=quantity)
        return self.render_json_response(self.response_dict, status=200)

    def get_model_field(self, tweet):
        '''Возвращает атрибут экземпляра класса Tweet, если он существует.'''
        if self.field is None:
            raise ImproperlyConfigured(
                "Значение атрибута 'field' не найдено."
            )
        attr = getattr(tweet, self.field, None)
        if attr is None:
            raise ImproperlyConfigured(
                f"Атрибут '{attr}' модели 'Tweet' не найден. Укажите корректный атрибут."
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
        '''Возвращает количество пользователей для найденного атрибута экземпляра класса модели Tweet.'''
        return self.model_field.count()
