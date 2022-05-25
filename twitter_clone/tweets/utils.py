import json
from utils.mixins import M2MEditMixin
from tweets.models import Tweet

class TweetActionsMixin(M2MEditMixin):
    '''
    Миксин для работы с M2M полями модели Tweet (likes, retweets, bookmarks).
    Получает id твита от клиента и добавляет/удаляет текущего пользователя у найденного экземпляра класса для указанного атрибута и
    отправляет соответствуютщий ответ клиенту в формате json.
    '''

    def post(self, request, *args, **kwargs):
        tweet_id = json.load(request)['tweet_id']

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
            self.model_field.add(request.user)
            self.response_dict.update(result='added')
        if action == 'remove':
            self.model_field.remove(request.user)
            self.response_dict.update(result='deleted')
        return super().post(request, *args, **kwargs)