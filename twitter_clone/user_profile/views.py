from django.views.generic import ListView, View
from django.shortcuts import get_object_or_404

from .utils import ProfileDataMixin
from tweets.models import Tweet
from tweets.forms import TweetForm
from authorization.models import CustomUser

# Create your views here.

class ProfileTweetsView(ProfileDataMixin, ListView):
    '''Отображает корневые твиты(не являющиеся ответами на другие) пользователя.'''

    template_name = 'user_profile/profile_tweets.html'
    context_object_name = 'root_tweets'

    def get_queryset(self):
        self.user = get_object_or_404(CustomUser, username=self.kwargs['username'])
        return Tweet.objects.filter(user__username=self.user.username, parent__isnull=True).order_by('-pub_date'). \
                select_related('user').prefetch_related('likes', 'retweets', 'children')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'{self.user.profile_name} (@{self.user.username})'
        return context

class ProfileRepliesView(ProfileDataMixin, ListView):
    '''Отображает твиты пользователя, которые ялвяются ответами на другие.'''

    template_name = 'user_profile/profile_replies.html'
    context_object_name = 'replies'

    def get_queryset(self):
        self.user = get_object_or_404(CustomUser, username=self.kwargs['username'])
        return Tweet.objects.filter(user__username=self.user.username, parent__isnull=False).order_by('-pub_date'). \
                select_related('user').prefetch_related('likes', 'retweets', 'children')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Твиты с ответами от {self.user.profile_name} (@{self.user.username})'
        return context

class ProfileMediaView(ProfileDataMixin, ListView):
    pass

class ProfileLikesView(ProfileDataMixin, ListView):
    '''Отображает твиты, которым текущий пользователь поставил лайк.'''

    template_name = 'user_profile/profile_likes.html'
    context_object_name = 'likes'

    def get_queryset(self):
        self.user = get_object_or_404(CustomUser, username=self.kwargs['username'])
        return self.user.liked_tweets.order_by('-tweetlike__timestamp'). \
                select_related('user').prefetch_related('likes', 'retweets', 'children')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Твиты, которые нравятся {self.user.profile_name} (@{self.user.username})'
        return context
