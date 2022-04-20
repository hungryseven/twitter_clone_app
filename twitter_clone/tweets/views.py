from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import View, ListView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import BaseCreateView
from django.db.models import Q

from braces.views import JSONResponseMixin

from .models import Tweet
from .forms import TweetForm
from .utils import TweetEditMixin
from main_app.utils import DataMixin
from authorization.models import CustomUser

class DetailtTweetView(DataMixin, SingleObjectMixin, ListView):
    '''Отображает главный/детальный твит на странице, а также всех его предков и потомков.'''

    template_name = 'tweets/detail_tweet.html'

    def get(self, request, *args, **kwargs):
        # Берем username из URL и проверяем, существует ли вообще такой пользователь, если нет, то выкидываем 404 ошибку.
        # Если такой пользователь существует, то поиск объекта происходит среди всех твитов, оставленных им.
        # Если у данного пользователь нет твита с запрашиваемым id, то выкидываем 404 ошибку.
        user = get_object_or_404(CustomUser, username=self.kwargs['username'])
        self.object = self.get_object(queryset=user.tweets.all().select_related('user'))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detail_tweet'] = self.object
        return context

    def get_queryset(self):
        # Находим всех предков текущего твита(включая сам твит) и всех его ближайших потомков(на один уровень ниже),
        # затем объединяем оба запроса и сортируем по lft значению в порядке возрастания.
        # Не используются методы django-mptt(get_ancestors и get_childen), т.к. они имеют встроенную сортировку,
        # из-за чего нельзя добиться необходимого поведения запроса.
        ancestors = Tweet.objects.filter(
            Q(lft__lte=self.object.lft) & Q(rght__gte=self.object.rght),
            tree_id=self.object.tree_id
        ).select_related('user').prefetch_related('likes', 'retweets', 'children')
        childrens = Tweet.objects.filter(
            Q(lft__gt=self.object.lft) & Q(rght__lt=self.object.rght),
            level=self.object.level+1,
            tree_id=self.object.tree_id
        ).select_related('user').prefetch_related('likes', 'retweets', 'children')
        return ancestors.union(childrens).order_by('lft')

class MakeTweetView(BaseCreateView):
    '''
    Обрабатывает форму и создает как корневые твиты,
    так и твиты, которые являются ответами(потомками) на другие твиты.
    '''

    form_class = TweetForm

    def form_valid(self, form):
        tweet = form.save(commit=False)

        # Получаем значение из скрытого поля формы. Если оно не пустое, то значением является id родительского твита.
        parent = self.request.POST['parent']
        if parent:
            tweet.parent_id = int(parent)

        tweet.user = self.request.user
        tweet.save()
        return super().form_valid(form)

    def get_success_url(self):
        '''После успешного создания твита, перенаправляет на страницу, с которой он был создан.'''
        return self.request.META.get('HTTP_REFERER', '/')

    def form_invalid(self):
        return HttpResponseRedirect(self.get_success_url())

class LikeTweetView(TweetEditMixin, View):
    '''Обрабатывает лайк определенного твита для текущего пользователя.'''

    field = 'likes'
    action = 'add'
    calculate_quantity = True

class DislikeTweetView(TweetEditMixin, View):
    '''Обрабатывает дизлайк/отмену лайка определенного твита для текущего пользователя.'''

    field = 'likes'
    action = 'remove'
    calculate_quantity = True

class RetweetView(TweetEditMixin, View):
    '''Обрабатывает ретвит определенного твита для текущего пользователя.'''

    field = 'retweets'
    action = 'add'
    calculate_quantity = True

class CancelRetweetView(TweetEditMixin, View):
    '''Обрабатывает отмену ретвита определенного твита для текущего пользователя.'''

    field = 'retweets'
    action = 'remove'
    calculate_quantity = True

class AddTweetToBookmarksView(TweetEditMixin, View):
    '''Обрабатывает добавление определенного твита в закладки для текущего пользователя.'''

    field = 'bookmarks'
    action = 'add'
    response_dict = {
        'btn_text': 'Удалить твит из закладок',
        'success_message': 'Твит добавлен в закладки'
    }

class DeleteTweetFromBookmarksView(TweetEditMixin, View):
    '''Обрабатывает удаление определенного твита из закладок для текущего пользователя.'''
    
    field = 'bookmarks'
    action = 'remove'
    response_dict = {
        'btn_text': 'Закладка',
        'success_message': 'Твит удален из закладок'
    }

class UserActionsApiView(JSONResponseMixin, View):
    '''
    Получает информацию о id всех лайкнутых/ретвитнутых/добавленных в закладки твитах для текущего пользователя
    и возвращает ответ в формате json.
    '''

    def get(self, request, *args, **kwargs):
        user = self.request.user
        likes = [tweet.id for tweet in user.liked_tweets.all()]
        retweets = [tweet.id for tweet in user.retweeted_tweets.all()]
        bookmarks = [tweet.id for tweet in user.bookmarked_tweets.all()]
        context_dict = {
            'likes': likes,
            'retweets': retweets,
            'bookmarks': bookmarks
        }
        return self.render_json_response(context_dict)