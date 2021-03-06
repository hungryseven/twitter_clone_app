from django.views.generic import ListView, TemplateView
from django.db.models import Q, F, Value, BigIntegerField

from tweets.models import Tweet, FIELDS_TO_PREFETCH
from utils.mixins import DataMixin

# Create your views here.

class HomeView(DataMixin, ListView):
    '''
    Отображает твиты и ретвиты текущего авторизованного пользователя,
    а также твиты и ретвиты всех пользователей, на которых он подписан.
    '''

    template_name = 'main_app/home.html'
    context_object_name = 'tweets'

    def get_queryset(self):
        user = self.request.user
        # Находим все твиты(как корневые, так и реплаи) текущего авторизованного пользователя
        # и всех пользотелей, на которых он подписан.
        tweets = Tweet.objects.filter(Q(user=user) | Q(user__in=user.followees.all())). \
                    annotate(action_time=F('pub_date'), retweeted_by=Value(0, output_field=BigIntegerField())). \
                    select_related('user').prefetch_related(*FIELDS_TO_PREFETCH)
                    
        # Находим все ретвиты текущего авторизованного пользователя
        # и всех пользователей, на которых он подписан.
        retweets = Tweet.objects.filter(Q(tweetretweet__user=user) | Q(tweetretweet__user__in=user.followees.all())). \
                    annotate(action_time=F('tweetretweet__timestamp'), retweeted_by=F('tweetretweet__user')). \
                    select_related('user').prefetch_related(*FIELDS_TO_PREFETCH)
        return tweets.union(retweets).order_by('-action_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная'
        return context

class Error404View(DataMixin, TemplateView):

    template_name = 'main_app/404.html'

class Error505View(DataMixin, TemplateView):

    template_name = 'main_app/505.html'