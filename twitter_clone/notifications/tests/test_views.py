from django.test import TestCase
from django.urls import reverse

from authorization.models import CustomUser
from tweets.models import Tweet

class SetUpMixin:

    def setUp(self):
        self.user1 = CustomUser.objects.create_user(username='user1', email='user1@test.com', profile_name='user1', password='Password1')
        self.user2 = CustomUser.objects.create_user(username='user2', email='user2@test.com', profile_name='user2', password='Password2')

    def login_user1(self):
        return self.client.login(username='user1', password='Password1')

class MentionsViewTests(SetUpMixin, TestCase):
    '''
    Тесты для представления, в котором отображаются твиты,
    в которых был упомянут текущий авторизованный пользователь,
    кроме созданных этим же пользователем.
    '''

    def setUp(self):
        return super().setUp()

    def test_view_url_inaccessible_for_unauthorized(self):
        '''Проверяет, что пользователь не авторизован и переводит его на страницу логина.'''
        response = self.client.get(reverse('notifications:mentions'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/')

    def test_view_url_accessible_by_name(self):
        '''Проверяет, что страница доступна по имени url паттерна.'''
        login = self.login_user1()
        response = self.client.get(reverse('notifications:mentions'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request['PATH_INFO'], '/notifications/mentions/')

    def test_view_uses_correct_template(self):
        '''Проверяет, что представление использует нужный шаблон.'''
        login = self.login_user1()
        response = self.client.get(reverse('notifications:mentions'))
        self.assertTemplateUsed(response, 'notifications/mentions.html')

    def test_view_with_mentions_in_other_users_tweets_only(self):
        '''
        Если текущий авторизованный пользователь был упомянут в твитах,
        которые были созданы любым другим пользователем, кром него,
        то отображает эти твиты в порядке их создания от недавнего
        до самого старого.
        '''
        # Создаем 2 твита пользователем "user2" с упоминанием "user1" в них
        tweet1 = Tweet.objects.create(text=f'mention1 for @{self.user1.username}', user=self.user2)
        tweet2 = Tweet.objects.create(text=f'mention2 for @{self.user1.username}', user=self.user2)

        login = self.login_user1()
        response = self.client.get(reverse('notifications:mentions'))
        self.assertQuerysetEqual(response.context['object_list'], [tweet2, tweet1])

    def test_view_with_mentions_in_all_tweets(self):
        '''
        Если текущий авторизованный пользователь был упомянут в каких-либо твитах
        (созданных другими пользователями и текущим пользователем),
        то отображает только твиты, созданные другими пользователями,
        в порядке их создания от недавнего до самого старого.
        '''
        # Создаем 3 твита пользователем "user2" и 1 твит пользователем user1 
        # с упоминанием "user1" в них
        tweet1 = Tweet.objects.create(text=f'mention1 for @{self.user1.username}', user=self.user2)
        tweet2 = Tweet.objects.create(text=f'mention2 for @{self.user1.username}', user=self.user1)
        tweet3 = Tweet.objects.create(text=f'mention3 for @{self.user1.username}', user=self.user2)

        login = self.login_user1()
        response = self.client.get(reverse('notifications:mentions'))
        self.assertQuerysetEqual(response.context['object_list'], [tweet3, tweet1])

    def test_unread_notifications(self):
        '''
        Если у текущего авторизованного пользователя существуют непрочитанные уведомления,
        то до перехода на страницу уведомлений в контексте и на страницах находится
        их количество. При переходе на страницу с уведомлениями все непрочитанные уведомления
        получают статус прочитанных.
        '''
        # Создаем 4 твита пользователем "user2" и 1 твит пользователем user1 
        # с упоминанием "user1" в них
        tweet1 = Tweet.objects.create(text=f'mention1 for @{self.user1.username}', user=self.user2)
        tweet2 = Tweet.objects.create(text=f'mention2 for @{self.user1.username}', user=self.user1)
        tweet3 = Tweet.objects.create(text=f'mention3 for @{self.user1.username}', user=self.user2)
        tweet4 = Tweet.objects.create(text=f'mention4 for @{self.user1.username}', user=self.user2)

        login = self.login_user1()

        # При переходе на любую страницу, кроме уведомлений,
        # у пользователя будут отображаться непрочитанные уведомления.
        response = self.client.get(reverse('main_app:home'))
        self.assertEqual(response.context['unread_notifications'], 3)

        # При переходе на странницу с уведомлениями все
        # непрочитанные уведомления получают статус прочитанных.
        response = self.client.get(reverse('notifications:mentions'))
        self.assertEqual(response.context['unread_notifications'], 0)
