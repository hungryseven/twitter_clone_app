from django.views.generic import TemplateView, ListView
from django.db.models import Q

from authorization.models import CustomUser
from tweets.models import Tweet
from utils.mixins import DataMixin

# Create your views here.

class ExploreView(DataMixin, TemplateView):

    template_name = 'explore/explore.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Обзор'
        return context

class SearchView(DataMixin, ListView):
    
    template_name = 'explore/search.html'
    context_object_name = 'searched_objects'

    def get_queryset(self):
        self.f = self.request.GET.get('f')
        self.q = self.request.GET.get('q')
        # Возвращает твиты, текст которых содержит запрашиваему строку, игнорируя регистр,
        # в порядке времени от недавнего до самого старого.
        if self.f == 'live':
            return Tweet.objects.filter(text__icontains=self.q).order_by('-pub_date'). \
                    select_related('user').prefetch_related('likes', 'retweets', 'children', 'mentioned_users')

        # Возвращает пользователей, в имени пользователя(юзернейме) или в имени профиля которых
        # содержится запрашиваемая строга, игнорируя регистр.
        if self.f == 'user':
            return CustomUser.objects.filter(Q(username__icontains=self.q) | Q(profile_name__icontains=self.q)).prefetch_related('followees')
        return Tweet.objects.filter(text__icontains=self.q)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Устанавливаем начальные значения полей формы
        if self.f or self.q:
            context['search_form'].initial.update(q=self.q)
            context['search_form'].initial.update(f=self.f)

        context['q'] = self.q
        context['f'] = self.f
        context['title'] = f'{self.q} - Поиск в Твиттере'
        return context

