from django.views.generic import ListView

from utils.mixins import DataMixin, SimpleLoginRequiredMixin

# Create your views here.

class BookmarksView(SimpleLoginRequiredMixin, DataMixin, ListView):
    '''
    Отображает все твиты, которые находятся в закладках у текущего авторизованного пользователя,
    в порядке времени от недавно добавленного в закладки твита до самого старого.
    '''
    
    template_name = 'bookmarks/bookmarks.html'
    context_object_name = 'bookmarks'

    def get_queryset(self):
        return self.request.user.bookmarked_tweets.order_by('-tweetbookmark__timestamp'). \
                select_related('user').prefetch_related('likes', 'retweets', 'children', 'mentioned_users', 'related_tags')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Закладки'
        return context