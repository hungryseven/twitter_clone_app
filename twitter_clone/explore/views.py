import datetime

from django.views.generic import TemplateView, ListView
from django.db.models import Q, Count
from django.utils import timezone

from authorization.models import CustomUser
from tweets.models import Tweet, Tag
from utils.mixins import DataMixin

# Create your views here.

class ExploreView(DataMixin, TemplateView):
    '''Отображает форму для поиска по твитам и пользователям.'''

    template_name = 'explore/explore.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Обзор'
        return context

class SearchView(DataMixin, ListView):
    '''
    Обрабатывает форму поиска по твитам и пользователям в зависимости от запроса.
    '''
    
    template_name = 'explore/search.html'
    context_object_name = 'searched_objects'

    def get_queryset(self):
        self.q = self.request.GET['q']
        self.f = self.request.GET['f']

        # Поиск для вкладки "Популярное".
        # Популярное формируется из твитов, написанных в течение прошлых 7 дней от текущего момента,
        # у которых сумма ответов(прямых потомков), лайков и ретвитов >= 10.
        if not self.f:
            week_ago = timezone.now() - datetime.timedelta(days=7)
            # Если "#" - первый символ в поисковом запросе, то ищем объект тега и связанные с ним твиты.
            if self.q[0] == '#':
                try:
                    tag = Tag.objects.get(tag_name=self.q)
                except Tag.DoesNotExist:
                    return []
                return tag.related_tweets. \
                        annotate(actions_count=Count('likes', distinct=True)+Count('retweets', distinct=True)+Count('children', distinct=True)). \
                        filter(pub_date__gte=week_ago, actions_count__gte=10).order_by('-actions_count'). \
                        select_related('user').prefetch_related('likes', 'retweets', 'children', 'mentioned_users', 'related_tags')

            # В противном случае ищем твиты, содержащие в тексте переданный поисковой запрос без учета регистра.
            return Tweet.objects. \
                    annotate(actions_count=Count('likes', distinct=True)+Count('retweets', distinct=True)+Count('children', distinct=True)). \
                    filter(text__icontains=self.q, pub_date__gte=week_ago, actions_count__gte=10).order_by('-actions_count'). \
                    select_related('user').prefetch_related('likes', 'retweets', 'children', 'mentioned_users', 'related_tags')
        
        # Поиск для вкладки "Последнее".
        if self.f == 'live':
            if self.q[0] == '#':
                try:
                    tag = Tag.objects.get(tag_name=self.q)
                except Tag.DoesNotExist:
                    return []
                return tag.related_tweets.order_by('-pub_date'). \
                    select_related('user').prefetch_related('likes', 'retweets', 'children', 'mentioned_users', 'related_tags')
            return Tweet.objects.filter(text__icontains=self.q).order_by('-pub_date'). \
                    select_related('user').prefetch_related('likes', 'retweets', 'children', 'mentioned_users', 'related_tags')

        # Поиск для вкладки "Люди".
        if self.f == 'user':
            # Если "#" - первый символ в поисковом запросе, то обрезаем его.
            query = self.q[1:] if self.q[0] == '#' else self.q
            # Ищем пользователей, в юзернейме или имени профиля которых
            # содержится запрашиваемая строка без учета регистра.
            return CustomUser.objects.filter(Q(username__icontains=query) | Q(profile_name__icontains=query)).prefetch_related('followees')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Устанавливаем начальные значения полей формы
        if self.f or self.q:
            context['search_form'].initial.update(q=self.q, f=self.f)

        context['q'] = self.q
        context['f'] = self.f
        context['title'] = f'{self.q} - Поиск в Твиттере'
        return context

