from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, View
from django.views.generic.edit import BaseUpdateView
from django.db.models import F

from braces.views import JSONResponseMixin

from utils.mixins import LoginRequiredAjaxMixin
from .utils import ProfileDataMixin, UserFollowMixin
from .forms import UpdateProfileForm
from tweets.models import Tweet

# Create your views here.

class ProfileTweetsView(ProfileDataMixin, ListView):
    '''Отображает корневые твиты(не являющиеся ответами на другие) и ретвиты пользователя.'''

    template_name = 'user_profile/profile_tweets.html'
    context_object_name = 'root_tweets'

    def get_queryset(self):
        self.user = self.get_user()

        # Находим корневые твиты и ретвиты найденного пользователя.
        # Вводим новую колонку с временем совершения действия(время создания твита и время ретвита),
        # объединяем запросы и сортируем по этой колонке.
        user_tweets = Tweet.objects.filter(user__username=self.user.username, parent__isnull=True).annotate(action_time=F('pub_date')). \
                select_related('user').prefetch_related('likes', 'retweets', 'children')
        user_retweets = self.user.retweeted_tweets.annotate(action_time=F('tweetretweet__timestamp')). \
                select_related('user').prefetch_related('likes', 'retweets', 'children')
        return user_tweets.union(user_retweets).order_by('-action_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'{self.user.profile_name} (@{self.user.username})'
        return context

class ProfileRepliesView(ProfileDataMixin, ListView):
    '''Отображает твиты пользователя, которые ялвяются ответами на другие.'''

    template_name = 'user_profile/profile_replies.html'
    context_object_name = 'replies'

    def get_queryset(self):
        self.user = self.get_user()
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
        self.user = self.get_user()
        return self.user.liked_tweets.order_by('-tweetlike__timestamp'). \
                select_related('user').prefetch_related('likes', 'retweets', 'children')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Твиты, которые нравятся {self.user.profile_name} (@{self.user.username})'
        return context

class UpdateProfileView(JSONResponseMixin, BaseUpdateView):
    '''Обрабатывает форму и обновляет информацию о пользователе в профиле.'''

    form_class = UpdateProfileForm

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        '''После успешного обновления информации в профиле, перенаправляет на страницу, с которой он был создан.'''
        return self.request.META.get('HTTP_REFERER', '/')

    def form_invalid(self, form):
        return HttpResponseRedirect(self.get_success_url())

class FollowersView(ProfileDataMixin, ListView):
    '''Отображает всех подписчиков данного пользователя.'''
    
    template_name = 'user_profile/followers.html'
    context_object_name = 'followers'

    def get_queryset(self):
        self.user = self.get_user()
        return self.user.followers.all().prefetch_related('followees')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Люди, которые читают {self.user.profile_name} (@{self.user.username})'
        return context

class FollowingView(ProfileDataMixin, ListView):
    '''Отображает всех пользователей, на которых подписан данный пользователь.'''
    
    template_name = 'user_profile/followees.html'
    context_object_name = 'followees'

    def get_queryset(self):
        self.user = self.get_user()
        return self.user.followees.all().prefetch_related('followees')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Люди, которых читает {self.user.profile_name} (@{self.user.username})'
        return context

class FollowersYouFollowView(ProfileDataMixin, ListView):
    '''Отображает подписчиков данного пользователя, на которых подписан текущий пользователь, если они есть.'''

    template_name = 'user_profile/followers_user_follow.html'
    context_object_name = 'familiar_followers'

    def get(self, request, *args, **kwargs):
        self.user = self.get_user()

        # Если текущий авторизованный пользователь попытается зайти на данную страницу,
        # то произойдет редирект на страницу с его подписчиками.
        if self.user == request.user:
            return HttpResponseRedirect(reverse('user_profile:user_followers', kwargs={'username': request.user.username}))
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.get_users_followers_intersection()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Ваши знакомые, которые читают пользователя {self.user.profile_name} (@{self.user.username})'
        return context

class FollowUserView(UserFollowMixin, View):
    '''Обрабатывает добавление пользователя в отслеживаемое(подписки) текущего пользователя.'''

    field = 'followees'
    action = 'add'

class UnfollowUserView(UserFollowMixin, View):
    '''Обрабатывает удаление пользователя из отслеживаемого(подпискок) текущего пользователя.'''

    field = 'followees'
    action = 'remove'

class UserFollowApiView(JSONResponseMixin, View):
    '''
    Получает id всех пользователей, на которых подписан текущий пользователь,
    и возвращает ответ в формате json.
    '''

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            folowees = [user.id for user in user.followees.all()]
            context_dict = {
                'folowees': folowees
            }
            return self.render_json_response(context_dict)
        return self.render_json_response({'user': str(user)})
