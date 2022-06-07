from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, View
from django.views.generic.edit import BaseUpdateView
from django.db.models import F, Value, BigIntegerField

from braces.views import JSONResponseMixin

from utils.mixins import SimpleLoginRequiredMixin, SimpleLoginRequiredAjaxMixin
from .utils import ProfileDataMixin, UserFollowMixin
from .forms import UpdateProfileForm
from authorization.models import CustomUser
from tweets.models import Tweet, FIELDS_TO_PREFETCH

# Create your views here.

class ProfileTweetsView(ProfileDataMixin, ListView):
    '''
    Отображает корневые твиты(не являющиеся ответами на другие) и ретвиты пользователя
    в порядке от недавнего к самому старому.
    '''

    template_name = 'user_profile/profile_tweets.html'
    context_object_name = 'root_tweets'

    def get_queryset(self):
        self.user = self.get_user()

        # Находим корневые твиты и ретвиты найденного пользователя.
        # Вводим новую колонку с временем совершения действия(время создания твита и время ретвита),
        # объединяем запросы и сортируем по этой колонке.
        user_tweets = self.user.tweets.filter(parent__isnull=True). \
                        annotate(action_time=F('pub_date'), retweeted_by=Value(0, output_field=BigIntegerField())). \
                        select_related('user').prefetch_related(*FIELDS_TO_PREFETCH)
        user_retweets = self.user.retweeted_tweets. \
                        annotate(action_time=F('tweetretweet__timestamp'), retweeted_by=Value(self.user.pk, output_field=BigIntegerField())). \
                        select_related('user').prefetch_related(*FIELDS_TO_PREFETCH)
        return user_tweets.union(user_retweets).order_by('-action_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'{self.user.profile_name} (@{self.user.username})'
        return context

class ProfileRepliesView(SimpleLoginRequiredMixin, ProfileDataMixin, ListView):
    '''
    Отображает твиты пользователя, которые ялвяются ответами на другие,
    в порядке от недавнего к самому старому.
    '''

    template_name = 'user_profile/profile_replies.html'
    context_object_name = 'replies'

    def get_queryset(self):
        self.user = self.get_user()
        return Tweet.objects.filter(user__username=self.user.username, parent__isnull=False).order_by('-pub_date'). \
                select_related('user').prefetch_related(*FIELDS_TO_PREFETCH)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Твиты с ответами от {self.user.profile_name} (@{self.user.username})'
        return context

class ProfileLikesView(SimpleLoginRequiredMixin, ProfileDataMixin, ListView):
    '''
    Отображает твиты, которым текущий пользователь поставил лайк,
    в порядке от недавнего к самому старому. 
    '''

    template_name = 'user_profile/profile_likes.html'
    context_object_name = 'likes'

    def get_queryset(self):
        self.user = self.get_user()
        return self.user.liked_tweets.order_by('-tweetlike__timestamp'). \
                select_related('user').prefetch_related(*FIELDS_TO_PREFETCH)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Твиты, которые нравятся {self.user.profile_name} (@{self.user.username})'
        return context

class UpdateProfileView(BaseUpdateView):
    '''Обрабатывает форму и обновляет информацию о пользователе в профиле.'''

    form_class = UpdateProfileForm

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        '''После успешного обновления информации в профиле, перенаправляет на страницу, с которой она была обновлена.'''
        return self.request.META.get('HTTP_REFERER', '/')

    def form_invalid(self, form):
        return HttpResponseRedirect(self.get_success_url())

class FollowersView(SimpleLoginRequiredMixin, ProfileDataMixin, ListView):
    '''
    Отображает всех подписчиков данного пользователя в порядке добавления
    текущего пользователя в читаемое(от последнего подписавшегося до
    самого первого).
    '''
    
    template_name = 'user_profile/followers.html'
    context_object_name = 'followers'

    def get_queryset(self):
        self.user = self.get_user()
        return CustomUser.objects.filter(followees=self.user).order_by('-followee_set__timestamp').prefetch_related('followees')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Люди, которые читают {self.user.profile_name} (@{self.user.username})'
        return context

class FollowingView(SimpleLoginRequiredMixin, ProfileDataMixin, ListView):
    '''
    Отображает всех пользователей, на которых подписан данный пользователь,
    в порядке добавления их текущим пользователем в читаемое(от последней подписки до
    самой первой).
    '''
    
    template_name = 'user_profile/followees.html'
    context_object_name = 'followees'

    def get_queryset(self):
        self.user = self.get_user()
        return CustomUser.objects.filter(followers=self.user).order_by('-follower_set__timestamp').prefetch_related('followees')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Люди, которых читает {self.user.profile_name} (@{self.user.username})'
        return context

class FollowersYouFollowView(SimpleLoginRequiredMixin, ProfileDataMixin, ListView):
    '''
    Отображает подписчиков данного пользователя, на которых подписан текущий пользователь(пересечение подписчиков),
    если они есть. Отображает их в в порядке добавления текущего пользователя в читаемое(от последнего подписавшегося до
    самого первого).
    '''

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

class FollowUserView(SimpleLoginRequiredAjaxMixin, UserFollowMixin, View):
    '''
    Обрабатывает добавление пользователя в отслеживаемое(подписки)
    текущего авторизованного пользователя.
    '''

    field = 'followees'
    action = 'add'

class UnfollowUserView(SimpleLoginRequiredAjaxMixin, UserFollowMixin, View):
    '''
    Обрабатывает удаление пользователя из отслеживаемого(подпискок)
    текущего авторизованного пользователя.
    '''

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
            followees = [user.id for user in user.followees.all()]
            context_dict = {
                'followees': followees
            }
            return self.render_json_response(context_dict)
        return self.render_json_response({'user': str(user)})
