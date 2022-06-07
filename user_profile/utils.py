import json
from django.shortcuts import get_object_or_404
from utils.mixins import DataMixin, M2MEditMixin
from .forms import UpdateProfileForm
from authorization.models import CustomUser

class ProfileDataMixin(DataMixin):
    '''Миксин с данными, которые используются на всех страницах профиля пользователя.'''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Экземпляр класса CustomUser для профиля, в котором находится текущий пользователь
        context['profile_owner'] = self.user

        if self.request.user.is_authenticated:
            context['familiar_followers'] = self.get_users_followers_intersection()
            context['profile_form'] = UpdateProfileForm(
                initial={
                    'profile_name': self.request.user.profile_name,
                    'about': self.request.user.about,
                    'location': self.request.user.location,
                    'website': self.request.user.website
                }
            )
        return context

    def get_user(self):
        '''Возвращает объект по имени пользователя из адресной строки или 404 ошибку.'''
        return get_object_or_404(CustomUser, username=self.kwargs['username'])

    def get_users_followers_intersection(self):
        '''
        Возвращает пересечение подписчиков данного и текущего пользователей,
        т.е. тех пользователей, на которых подписаны оба.
        '''
        # Находим всех подписчиков пользователя, на странице которого находится текущий авторизованный.
        # Затем находим всех совпадающих подписчиков текущего авторизованного пользователя и
        # владельца страницы, на которой он находится, отсортированных по времени добавления
        # текущего авторизованного пользователя в читаемое.
        profile_owner_followers = self.user.followers.all()
        return CustomUser.objects.filter(followees=self.request.user, pk__in=profile_owner_followers). \
                                    order_by('-followee_set__timestamp').prefetch_related('followees')

class UserFollowMixin(M2MEditMixin):
    '''
    Миксин для работы с M2M полями модели CustomUser(followers, followees).
    Получает id твита от клиента и добавляет/удаляет найденного пользователя у текущего экземпляра класса для указанного атрибута и
    отправляет соответствуютщий ответ клиенту в формате json.
    '''

    def post(self, request, *args, **kwargs):
        user_id = json.load(request)['user_id']

        # Проверяем, существует ли объект с таким id.
        # Если нет, то выкидываем ошибку и возвращаем ответ.
        try:
            user = CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            self.response_dict.update(error=self.error_message)
            return self.render_json_response(self.response_dict, status=500)
        
        # Если найденный пользователь является текущим,
        # то выкидываем ошибку и возвращаем ответ.
        if user.username == request.user.username:
            self.response_dict.update(error=self.error_message)
            return self.render_json_response(self.response_dict, status=500)

        self.model_field = self.get_model_field(request.user)
        action = self.get_action()
        if action == 'add':
            self.model_field.add(user)
            self.response_dict.update(result='followed')
        if action == 'remove':
            self.model_field.remove(user)
            self.response_dict.update(result='unfollowed')
        return super().post(request, *args, **kwargs)