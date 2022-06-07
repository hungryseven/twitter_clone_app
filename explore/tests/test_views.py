from django.test import TestCase
from django.urls import reverse

from authorization.models import CustomUser
from tweets.models import Tweet
from utils.funcs import build_url

class SetUpMixin:

    def setUp(self):
        for i in range(1, 11):
            CustomUser.objects.create_user(username=f'user{i}', email=f'user{i}@test.com', profile_name=f'user{i}', password=f'Password{i}')

        self.tweet1 = Tweet.objects.create(text='popular tweet1 #tweet', user=CustomUser.objects.get(username='user1'))
        self.tweet2 = Tweet.objects.create(text='popular tweet2 #tweet', user=CustomUser.objects.get(username='user2'))
        self.tweet3 = Tweet.objects.create(text='simple tweet1 #tweet', user=CustomUser.objects.get(username='user3'))
        self.tweet4 = Tweet.objects.create(text='simple tweet2 #tweet', user=CustomUser.objects.get(username='user4'))

class ExploreViewTest(TestCase):
    '''Тесты для представления, которое отображает страницу "Обзор".'''

    def test_view_url_accessible_by_name(self):
        '''Проверяет, что страница доступна по имени url паттерна.'''
        response = self.client.get(reverse('explore:explore'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request['PATH_INFO'], f'/explore/')

    def test_view_uses_correct_template(self):
        '''Проверяет, что представление использует нужный шаблон.'''
        response = self.client.get(reverse('explore:explore'))
        self.assertTemplateUsed(response, 'explore/explore.html')

class SearchViewTest(SetUpMixin, TestCase):
    '''Тесты для представления, которое осуществляет поиск по твитам и пользователям.'''

    def test_view_popular_url_accessible_by_name(self):
        '''Проверяет, что страница с вкладкой "Популярное" доступна по имени url паттерна.'''
        response = self.client.get(
            build_url(
                'explore:search',
                get={'q': 'query', 'f': ''}
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request['PATH_INFO'], f'/search/')
        self.assertEqual(response.request['QUERY_STRING'], f'q=query&f=')

    def test_view_latest_url_accessible_by_name(self):
        '''Проверяет, что страница с вкладкой "Последнее" доступна по имени url паттерна.'''
        response = self.client.get(
            build_url(
                'explore:search',
                get={'q': 'query', 'f': 'live'}
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request['PATH_INFO'], f'/search/')
        self.assertEqual(response.request['QUERY_STRING'], f'q=query&f=live')

    def test_view_users_url_accessible_by_name(self):
        '''Проверяет, что страница с вкладкой "Пользователи" доступна по имени url паттерна.'''
        response = self.client.get(
            build_url(
                'explore:search',
                get={'q': 'query', 'f': 'user'}
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request['PATH_INFO'], f'/search/')
        self.assertEqual(response.request['QUERY_STRING'], f'q=query&f=user')

    def test_view_uses_correct_template(self):
        '''Проверяет, что представление использует нужный шаблон.'''
        response = self.client.get(
            build_url(
                'explore:search',
                get={'q': 'query', 'f': ''}
            )
        )
        self.assertTemplateUsed(response, 'explore/search.html')

    def test_view_empty_popular_tab(self):
        '''Тест вкладки "Популярное", если для тега/запроса нет твитов.'''
        # Поиск по тегу.
        response = self.client.get(
            build_url(
                'explore:search',
                get={'q': '#empty', 'f': ''}
            )
        )
        self.assertQuerysetEqual(response.context['object_list'], [])

        # Поисковой запрос.
        response = self.client.get(
            build_url(
                'explore:search',
                get={'q': 'empty', 'f': ''}
            )
        )
        self.assertQuerysetEqual(response.context['object_list'], [])

    def test_view_popular_tab(self):
        '''Тест вкладки "Популярное", если для тега/запроса такие твиты существуют.'''
        # Лайкаем и ретвитим всеми существующими юзерами tweet1, а также создаем реплаи к нему.
        # Аналогично поступаем с tweet2, только совершаем эти действия первыми 5 юзерами.
        users = CustomUser.objects.all()
        for i, user in enumerate(users, start=1):
            user.liked_tweets.add(self.tweet1)
            user.retweeted_tweets.add(self.tweet1)
            Tweet.objects.create(text=f'reply{i} by {user.username}', user=user, parent=self.tweet1)
            if i <= 5:
                user.liked_tweets.add(self.tweet2)
                user.retweeted_tweets.add(self.tweet2)
                Tweet.objects.create(text=f'reply{i} by {user.username}', user=user, parent=self.tweet2)

        # Поиск по тегу.
        response = self.client.get(
            build_url(
                'explore:search',
                get={'q': '#tweet', 'f': ''}
            )
        )
        self.assertQuerysetEqual(response.context['object_list'], [self.tweet1, self.tweet2])
        # Проверка суммы лайков, ретвитов и реплаев для каждого твита.
        actions_count = [tweet.actions_count for tweet in response.context['object_list']]
        self.assertListEqual(actions_count, [30, 15])

        # Поисковой запрос.
        response = self.client.get(
            build_url(
                'explore:search',
                get={'q': 'tweet', 'f': ''}
            )
        )
        self.assertQuerysetEqual(response.context['object_list'], [self.tweet1, self.tweet2])
        actions_count = [tweet.actions_count for tweet in response.context['object_list']]
        self.assertListEqual(actions_count, [30, 15])

    def test_view_empty_latest_tab(self):
        '''Тест вкладки "Последнее", если для тега/запроса нет твитов.'''
        # Поиск по тегу.
        response = self.client.get(
            build_url(
                'explore:search',
                get={'q': '#empty', 'f': 'live'}
            )
        )
        self.assertQuerysetEqual(response.context['object_list'], [])

        # Поисковой запрос.
        response = self.client.get(
            build_url(
                'explore:search',
                get={'q': 'empty', 'f': 'live'}
            )
        )
        self.assertQuerysetEqual(response.context['object_list'], [])

    def test_view_latest_tab(self):
        '''Тест вкладки "Последнее", если для тега/запроса такие твиты существуют.'''
        # Поиск по тегу.
        response = self.client.get(
            build_url(
                'explore:search',
                get={'q': '#tweet', 'f': 'live'}
            )
        )
        self.assertQuerysetEqual(response.context['object_list'], [self.tweet4, self.tweet3, self.tweet2, self.tweet1])

        # Поисковой запрос.
        response = self.client.get(
            build_url(
                'explore:search',
                get={'q': 'tweet1', 'f': 'live'}
            )
        )
        self.assertQuerysetEqual(response.context['object_list'], [self.tweet3, self.tweet1])

    def test_view_empty_users_tab(self):
        '''Тест вкладки "Пользователи", если для тега/запроса нет пользователей.'''
        # Поиск по тегу.
        response = self.client.get(
            build_url(
                'explore:search',
                get={'q': '#no_user', 'f': 'user'}
            )
        )
        self.assertQuerysetEqual(response.context['object_list'], [])

        # Поисковой запрос.
        response = self.client.get(
            build_url(
                'explore:search',
                get={'q': 'no_user', 'f': 'user'}
            )
        )
        self.assertQuerysetEqual(response.context['object_list'], [])

    def test_view_users_tab(self):
        '''Тест вкладки "Пользователи", если для тега/запроса такие пользователи существуют.'''
        result = CustomUser.objects.filter(username__contains='1')

        # Поиск по тегу.
        response = self.client.get(
            build_url(
                'explore:search',
                get={'q': '#user1', 'f': 'user'}
            )
        )
        self.assertQuerysetEqual(response.context['object_list'], result, ordered=False)

        # Поисковой запрос.
        response = self.client.get(
            build_url(
                'explore:search',
                get={'q': 'user1', 'f': 'user'}
            )
        )
        self.assertQuerysetEqual(response.context['object_list'], result, ordered=False)