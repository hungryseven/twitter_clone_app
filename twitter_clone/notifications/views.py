from django.views.generic import ListView

from authorization.models import UserNotification
from utils.mixins import DataMixin, SimpleLoginRequiredMixin


# Create your views here.

class MentionsView(SimpleLoginRequiredMixin, DataMixin, ListView):
    '''
    Отображает все твиты, в которых был упомянут текущий авторизованный пользователь,
    кроме созданных этим же пользователем, в порядке времени от недавнего твита с
    уведомлением до самого старого.
    '''

    template_name = 'notifications/mentions.html'
    context_object_name = 'mentions'

    def get(self, request, *args, **kwargs):
        self.user = self.request.user
        # Если у текущего авторизованного пользователя есть непрочитанные уведомления,
        # то при заходе на страницу с ними их статус меняется.
        # Учитываются все твиты. Даже те, которые были созданы текущим пользователем,
        # в которых он упомянул сам себя.
        UserNotification.objects.filter(user=self.user, is_viewed=False).update(is_viewed=True)
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.user.notifications.exclude(user=self.user).order_by('-pub_date'). \
                select_related('user').prefetch_related('likes', 'retweets', 'children', 'mentioned_users', 'related_tags')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Уведомления'
        return context
