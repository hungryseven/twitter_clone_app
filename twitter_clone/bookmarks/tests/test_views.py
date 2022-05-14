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

class BookmarksViewTests(SetUpMixin, TestCase):
    '''
    Тесты для представления, в котором отображаются твиты,
    которые были добавлены в закладки текущим авторизованным пользователем.
    '''

    def test_view_url_inaccessible_for_unauthorized(self):
        '''Проверяет, что пользователь не авторизован и переводит его на страницу логина.'''
        response = self.client.get(reverse('bookmarks:bookmarks'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/')

    def test_view_url_accessible_by_name(self):
        '''Проверяет, что страница доступна по имени url паттерна.'''
        login = self.login_user1()
        response = self.client.get(reverse('bookmarks:bookmarks'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request['PATH_INFO'], '/i/bookmarks/')

    def test_view_uses_correct_template(self):
        '''Проверяет, что представление использует нужный шаблон.'''
        login = self.login_user1()
        response = self.client.get(reverse('bookmarks:bookmarks'))
        self.assertTemplateUsed(response, 'bookmarks/bookmarks.html')

    def test_view_without_bookmarks(self):
        '''
        Если у текущего авторизованного пользователя нет закладок,
        то отображается пустая страница.
        '''
        login = self.login_user1()
        response = self.client.get(reverse('bookmarks:bookmarks'))
        self.assertQuerysetEqual(response.context['object_list'], [])

    def test_view_with_bookmarks(self):
        '''
        Если у текущего авторизованного пользователя есть закладки,
        то отображает их в порядке по времени добавления от недавнего
        твита до самого старого
        '''
        # Создаем 3 твита и добавляем их в закладки пользователю "user1"
        tweet1 = Tweet.objects.create(text=f'tweet1', user=self.user2)
        tweet2 = Tweet.objects.create(text=f'tweet2', user=self.user1)
        tweet3 = Tweet.objects.create(text=f'tweet3', user=self.user2)
        self.user1.bookmarked_tweets.add(tweet2)
        self.user1.bookmarked_tweets.add(tweet3)
        self.user1.bookmarked_tweets.add(tweet1)
        
        login = self.login_user1()
        response = self.client.get(reverse('bookmarks:bookmarks'))
        self.assertQuerysetEqual(response.context['object_list'], [tweet1, tweet3, tweet2])