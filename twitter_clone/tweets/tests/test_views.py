import json

from django.test import TestCase
from django.urls import reverse
from django.utils.encoding import force_str

from authorization.models import CustomUser
from tweets.models import Tweet

class SetUpMixin:

    def setUp(self):
        self.user1 = CustomUser.objects.create_user(username='user1', email='user1@test.com', profile_name='user1', password='Password1')
        self.user2 = CustomUser.objects.create_user(username='user2', email='user2@test.com', profile_name='user2', password='Password2')

        self.tweet1 = Tweet.objects.create(text='tweet1', user=self.user1)
        self.tweet2 = Tweet.objects.create(text='tweet2', user=self.user2)
        self.tweet3 = Tweet.objects.create(text='tweet3', user=self.user2, parent=self.tweet2)
        self.tweet4 = Tweet.objects.create(text='tweet4', user=self.user1, parent=self.tweet2)
        self.tweet5 = Tweet.objects.create(text='tweet5', user=self.user1, parent=self.tweet3)

    def login_user1(self):
        return self.client.login(username='user1', password='Password1')

class DetailtTweetViewTest(SetUpMixin, TestCase):
    '''Тесты для представления, которое отображает главный/детальный твит, всех его потомков и предков.'''

    def setUp(self):
        return super().setUp()

    def test_view_url_accessible_by_name(self):
        '''Проверяет, что страница доступна по имени url паттерна.'''
        response = self.client.get(
            reverse(
                'tweets:detail_tweet',
                kwargs={
                    'username': self.user1.username,
                    'pk': self.tweet1.pk
                }
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request['PATH_INFO'], f'/{self.user1.username}/status/{self.tweet1.pk}/')

    def test_view_url_for_non_existent_user(self):
        '''Проверяет, что страница недоступна, если пользователя не существует.'''
        response = self.client.get(
            reverse(
                'tweets:detail_tweet',
                kwargs={
                    'username': 'non_existent',
                    'pk': self.tweet1.pk
                }
            )
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.request['PATH_INFO'], f'/non_existent/status/{self.tweet1.pk}/')

    def test_view_url_for_someone_elses_tweet(self):
        '''Проверяет, что страница недоступна, если твит принадлежит другому пользователю.'''
        # Твит принадлежит self.user2
        response = self.client.get(
            reverse(
                'tweets:detail_tweet',
                kwargs={
                    'username': self.user1.username,
                    'pk': self.tweet2.pk 
                }
            )
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.request['PATH_INFO'], f'/{self.user1.username}/status/{self.tweet2.pk}/')

    def test_view_uses_correct_template(self):
        '''Проверяет, что представление использует нужный шаблон.'''
        response = self.client.get(
            reverse(
                'tweets:detail_tweet',
                kwargs={
                    'username': self.user1.username,
                    'pk': self.tweet1.pk
                }
            )
        )
        self.assertTemplateUsed(response, 'tweets/detail_tweet.html')

    def test_view_for_tweet_without_parents_and_childs(self):
        '''Если у твита нет предков и потомков, то отображает только его.'''
        response = self.client.get(
            reverse(
                'tweets:detail_tweet',
                kwargs={
                    'username': self.user1.username,
                    'pk': self.tweet1.pk
                }
            )
        )
        self.assertQuerysetEqual(response.context['object_list'], [self.tweet1])

    def test_view_for_tweet_with_childs_only(self):
        '''
        Если у твита есть потомки и нет предков, то отображает твиты в следующем порядке:
        главный/детальный твит
                |
        все потомки в порядке от самого старого до недавнего.
        '''
        response = self.client.get(
            reverse(
                'tweets:detail_tweet',
                kwargs={
                    'username': self.user2.username,
                    'pk': self.tweet2.pk
                }
            )
        )
        self.assertQuerysetEqual(response.context['object_list'], [self.tweet2, self.tweet3, self.tweet4])

    def test_view_for_tweet_with_parents_and_childs(self):
        '''
        Если у твита есть потомки и предки, то отображает твиты в следующем порядке:
        все предки в порядке иерархии
                |
        главный/детальный твит
                |
        все потомки в порядке от самого старого до недавнего.
        '''
        response = self.client.get(
            reverse(
                'tweets:detail_tweet',
                kwargs={
                    'username': self.user2.username,
                    'pk': self.tweet3.pk
                }
            )
        )
        self.assertQuerysetEqual(response.context['object_list'], [self.tweet2, self.tweet3, self.tweet5])

class LikeTweetViewTest(SetUpMixin, TestCase):
    '''
    Тесты для представления, которое обрабатывает лайк твита
    для текущего авторизованного пользователя.
    '''

    def setUp(self):
        return super().setUp()

    def test_view_for_unauthorized(self):
        '''
        Проверяет, что сервер отдает 401 ошибку
        и JSON содержит ключ с ошибкой, если пользователь не авторизован.
        '''
        response = self.client.post(
            reverse('tweets:like_tweet'),
            {'tweet_id': self.tweet1.pk},
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, 401)
        self.assertIn('error', json_response)

    def test_view_for_authorized_likes_tweet(self):
        '''
        Проверяет, что сервер отдает 200 ответ и соответствующий JSON,
        когда текущий авторизованный пользователь успешно лайкнул твит.
        '''
        login = self.login_user1()
        response = self.client.post(
            reverse('tweets:like_tweet'),
            {'tweet_id': self.tweet1.pk},
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response.get('quantity', ''), 1)
        self.assertTrue(json_response.get('result', '') == 'added')
        self.assertIn(self.tweet1, self.user1.liked_tweets.all())

    def test_view_for_authorized_likes_non_existent_tweet(self):
        '''
        Проверяет, что сервер отдает 500 ответ и JSON содержит ключ с ошибкой,
        когда текущий авторизованный пользователь пытается лайкнуть несуществующий твит.
        '''
        login = self.login_user1()
        non_existent_pk = Tweet.objects.last().pk + 2
        response = self.client.post(
            reverse('tweets:like_tweet'),
            {'tweet_id': non_existent_pk},
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, 500)
        self.assertIn('error', json_response)

class DislikeTweetViewTest(SetUpMixin, TestCase):
    '''
    Тесты для представления, которое обрабатывает дизлайк/отмену лайка
    твита для текущего авторизованного пользователя.
    '''

    def setUp(self):
        return super().setUp()

    def test_view_for_unauthorized(self):
        '''
        Проверяет, что сервер отдает 401 ошибку
        и JSON содержит ключ с ошибкой, если пользователь не авторизован.
        '''
        response = self.client.post(
            reverse('tweets:dislike_tweet'),
            {'tweet_id': self.tweet1.pk},
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, 401)
        self.assertIn('error', json_response)

    def test_view_for_authorized_dislikes_tweet(self):
        '''
        Проверяет, что сервер отдает 200 ответ и соответствующий JSON,
        когда текущий авторизованный пользователь успешно
        дизлайкнул/отменил лайк на твите.
        '''
        login = self.login_user1()
        self.user1.liked_tweets.add(self.tweet1)
        response = self.client.post(
            reverse('tweets:dislike_tweet'),
            {'tweet_id': self.tweet1.pk},
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response.get('quantity', ''), 0)
        self.assertTrue(json_response.get('result', '') == 'deleted')
        self.assertNotIn(self.tweet1, self.user1.liked_tweets.all())

    def test_view_for_authorized_likes_non_existent_tweet(self):
        '''
        Проверяет, что сервер отдает 500 ответ и JSON содержит ключ с ошибкой,
        когда текущий авторизованный пользователь пытается дизлайкнуть несуществующий твит.
        '''
        login = self.login_user1()
        non_existent_pk = Tweet.objects.last().pk + 2
        response = self.client.post(
            reverse('tweets:dislike_tweet'),
            {'tweet_id': non_existent_pk},
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, 500)
        self.assertIn('error', json_response)

class RetweetViewTest(SetUpMixin, TestCase):
    '''
    Тесты для представления, которое обрабатывает ретвит
    для текущего авторизованного пользователя.
    '''

    def setUp(self):
        return super().setUp()

    def test_view_for_unauthorized(self):
        '''
        Проверяет, что сервер отдает 401 ошибку
        и JSON содержит ключ с ошибкой, если пользователь не авторизован.
        '''
        response = self.client.post(
            reverse('tweets:retweet'),
            {'tweet_id': self.tweet1.pk},
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, 401)
        self.assertIn('error', json_response)

    def test_view_for_authorized_retweets_tweet(self):
        '''
        Проверяет, что сервер отдает 200 ответ и соответствующий JSON,
        когда текущий авторизованный пользователь успешно ретвитнул твит.
        '''
        login = self.login_user1()
        response = self.client.post(
            reverse('tweets:retweet'),
            {'tweet_id': self.tweet1.pk},
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response.get('quantity', ''), 1)
        self.assertTrue(json_response.get('result', '') == 'added')
        self.assertIn(self.tweet1, self.user1.retweeted_tweets.all())

    def test_view_for_authorized_retweets_non_existent_tweet(self):
        '''
        Проверяет, что сервер отдает 500 ответ и JSON содержит ключ с ошибкой,
        когда текущий авторизованный пользователь пытается ретвитнуть несуществующий твит.
        '''
        login = self.login_user1()
        non_existent_pk = Tweet.objects.last().pk + 2
        response = self.client.post(
            reverse('tweets:retweet'),
            {'tweet_id': non_existent_pk},
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, 500)
        self.assertIn('error', json_response)

class CancelRetweetViewTest(SetUpMixin, TestCase):
    '''
    Тесты для представления, которое обрабатывает отмену ретвита
    для текущего авторизованного пользователя.
    '''

    def setUp(self):
        return super().setUp()

    def test_view_for_unauthorized(self):
        '''
        Проверяет, что сервер отдает 401 ошибку
        и JSON содержит ключ с ошибкой, если пользователь не авторизован.
        '''
        response = self.client.post(
            reverse('tweets:cancel_retweet'),
            {'tweet_id': self.tweet1.pk},
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, 401)
        self.assertIn('error', json_response)

    def test_view_for_authorized_cancels_retweet(self):
        '''
        Проверяет, что сервер отдает 200 ответ и соответствующий JSON,
        когда текущий авторизованный пользователь успешно отменил ретвит.
        '''
        login = self.login_user1()
        self.user1.retweeted_tweets.add(self.tweet1)
        response = self.client.post(
            reverse('tweets:cancel_retweet'),
            {'tweet_id': self.tweet1.pk},
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response.get('quantity', ''), 0)
        self.assertTrue(json_response.get('result', '') == 'deleted')
        self.assertNotIn(self.tweet1, self.user1.retweeted_tweets.all())

    def test_view_for_authorized_cancels_retweet_for_non_existent_tweet(self):
        '''
        Проверяет, что сервер отдает 500 ответ и JSON содержит ключ с ошибкой,
        когда текущий авторизованный пользователь пытается отменить ретвит для несуществующего твита.
        '''
        login = self.login_user1()
        non_existent_pk = Tweet.objects.last().pk + 2
        response = self.client.post(
            reverse('tweets:cancel_retweet'),
            {'tweet_id': non_existent_pk},
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, 500)
        self.assertIn('error', json_response)

class AddTweetToBookmarksViewTest(SetUpMixin, TestCase):
    '''
    Тесты для представления, которое обрабатывает добавление твита в закладки
    для текущего авторизованного пользователя.
    '''

    def setUp(self):
        return super().setUp()

    def test_view_for_unauthorized(self):
        '''
        Проверяет, что сервер отдает 401 ошибку
        и JSON содержит ключ с ошибкой, если пользователь не авторизован.
        '''
        response = self.client.post(
            reverse('tweets:add_to_bookmarks'),
            {'tweet_id': self.tweet1.pk},
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, 401)
        self.assertIn('error', json_response)

    def test_view_for_authorized_bookmarks_tweet(self):
        '''
        Проверяет, что сервер отдает 200 ответ и соответствующий JSON,
        когда текущий авторизованный пользователь успешно добавил твит в закладки.
        '''
        login = self.login_user1()
        response = self.client.post(
            reverse('tweets:add_to_bookmarks'),
            {'tweet_id': self.tweet1.pk},
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json_response.get('result', '') == 'added')
        self.assertIn(self.tweet1, self.user1.bookmarked_tweets.all())

    def test_view_for_authorized_bookmarks_non_existent_tweet(self):
        '''
        Проверяет, что сервер отдает 500 ответ и JSON содержит ключ с ошибкой,
        когда текущий авторизованный пользователь пытается добавить в закладки несуществующий твит.
        '''
        login = self.login_user1()
        non_existent_pk = Tweet.objects.last().pk + 2
        response = self.client.post(
            reverse('tweets:add_to_bookmarks'),
            {'tweet_id': non_existent_pk},
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, 500)
        self.assertIn('error', json_response)

class DeleteTweetFromBookmarksViewTest(SetUpMixin, TestCase):
    '''
    Тесты для представления, которое обрабатывает удаление твита из закладок
    для текущего авторизованного пользователя.
    '''

    def setUp(self):
        return super().setUp()

    def test_view_for_unauthorized(self):
        '''
        Проверяет, что сервер отдает 401 ошибку
        и JSON содержит ключ с ошибкой, если пользователь не авторизован.
        '''
        response = self.client.post(
            reverse('tweets:delete_from_bookmarks'),
            {'tweet_id': self.tweet1.pk},
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, 401)
        self.assertIn('error', json_response)

    def test_view_for_authorized_deletes_form_bookmarks_tweet(self):
        '''
        Проверяет, что сервер отдает 200 ответ и соответствующий JSON,
        когда текущий авторизованный пользователь успешно удалил твит из закладок.
        '''
        login = self.login_user1()
        response = self.client.post(
            reverse('tweets:delete_from_bookmarks'),
            {'tweet_id': self.tweet1.pk},
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json_response.get('result', '') == 'deleted')
        self.assertNotIn(self.tweet1, self.user1.bookmarked_tweets.all())

    def test_view_for_authorized_deletes_from_bookmarks_non_existent_tweet(self):
        '''
        Проверяет, что сервер отдает 500 ответ и JSON содержит ключ с ошибкой,
        когда текущий авторизованный пользователь пытается удалить из закладок несуществующий твит.
        '''
        login = self.login_user1()
        non_existent_pk = Tweet.objects.last().pk + 2
        response = self.client.post(
            reverse('tweets:delete_from_bookmarks'),
            {'tweet_id': non_existent_pk},
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, 500)
        self.assertIn('error', json_response)

class UserActionsApiViewTests(SetUpMixin, TestCase):
    '''
    Тесты для представления, в котором возвращается JSON
    с лайками, ретвитами, закладками текущего авторизованного пользователя.
    '''
    
    def setUp(self):
        return super().setUp()

    def test_view_url_accessible_by_name(self):
        '''Проверяет, что страница доступна по имени url паттерна.'''
        response = self.client.get(reverse('tweets:actions_api'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request['PATH_INFO'], '/actions/api/')

    def test_view_for_unauthorized(self):
        '''Проверяет, что возвращается в JSON для анонимного пользователя.'''
        response = self.client.get(reverse('tweets:actions_api'))
        self.assertJSONEqual(force_str(response.content), {'user': 'AnonymousUser'})

    def test_view_for_authorized_without_actions(self):
        '''Проверяет, что возвращается в JSON для авторизованного пользователя без лайков, ретвитов и закладок.'''
        login = self.login_user1()
        response = self.client.get(reverse('tweets:actions_api'))
        self.assertJSONEqual(
            force_str(response.content),
            {
                'likes': [],
                'retweets': [],
                'bookmarks': []
            }
        )

    def test_view_for_authorized_with_actions(self):
        '''Проверяет, что возвращается в JSON для авторизованного пользователя с лайками, ретвитами и закладками.'''
        login = self.login_user1()
        self.user1.liked_tweets.add(self.tweet1, self.tweet2)
        self.user1.retweeted_tweets.add(self.tweet3, self.tweet4)
        self.user1.bookmarked_tweets.add(self.tweet5)
        response = self.client.get(reverse('tweets:actions_api'))
        self.assertJSONEqual(
            force_str(response.content),
            {
                'likes': [self.tweet1.pk, self.tweet2.pk],
                'retweets': [self.tweet3.pk, self.tweet4.pk],
                'bookmarks': [self.tweet5.pk]
            }
        )

class MakeTweetViewTests(SetUpMixin, TestCase):
    pass