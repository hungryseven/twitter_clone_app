from main_app.utils import DataMixin

class ProfileDataMixin(DataMixin):
    '''Миксин с данными, которые используются на всех страницах профиля пользователя.'''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.kwargs['username']
        return context