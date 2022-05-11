from django.views.generic import TemplateView, ListView

from utils.mixins import DataMixin, SimpleLoginRequiredMixin

# Create your views here.

class BookmarksView(SimpleLoginRequiredMixin, DataMixin, ListView):
    '''
    Отображает все твиты, которые находятся в закладках у текущего авторизованного пользователя.
    '''
    
    template_name = 'bookmarks/bookmarks.html'
    context_object_name = 'bookmarks'

    def get_queryset(self):
        return self.request.user.bookmarked_tweets.order_by('-tweetbookmark__timestamp')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Закладки'
        return context