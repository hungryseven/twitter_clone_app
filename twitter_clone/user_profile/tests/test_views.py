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

    def login_user1(self):
        return self.client.login(username='user1', password='Password1')

class ProfileTweetsViewTests(SetUpMixin, TestCase):
    '''Тесты для представления, в котором отображаются корневые твиты и ретвиты пользователя.'''
    
    def setUp(self):
        return super().setUp()

    def test_view_url_accessible_by_name(self):
        '''Проверяет, что страница доступна по имени url паттерна.'''
        response = self.client.get(reverse('user_profile:profile_tweets', kwargs={'username': self.user1.username}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request['PATH_INFO'], '/user1/')

    def test_view_uses_correct_template(self):
        '''Проверяет, что представление использует нужный шаблон.'''
        response = self.client.get(reverse('user_profile:profile_tweets', kwargs={'username': self.user1.username}))
        self.assertTemplateUsed(response, 'user_profile/profile_tweets.html')

    def test_view_without_user_root_tweets_n_retweets(self):
        '''Если у пользователя нет корневых твитов и ретвитов, то ничего не отображает.'''
        response = self.client.get(reverse('user_profile:profile_tweets', kwargs={'username': self.user1.username}))
        self.assertQuerysetEqual(response.context['object_list'], [])

    def test_view_with_user_root_tweets_only(self):
        '''Если у пользователя есть только корневые твиты, то отображает их по времени создания от позднего к раннему.'''
        # Создаем 3 твита и кладем их в перевернутый список.
        for i in range(3):
            Tweet.objects.create(text=f'tweet{i}', user=self.user1)
        tweets = reversed(list(self.user1.tweets.all()))

        response = self.client.get(reverse('user_profile:profile_tweets', kwargs={'username': self.user1.username}))
        self.assertQuerysetEqual(response.context['object_list'], tweets)

    def test_view_with_user_retweets_only(self):
        '''
        Если у пользователя есть только ретвиты, то отображает только их
        по времени от позднего к раннему(время ретвита, а не создания твита).
        '''
        # Создаем 3 твита, добавляем их в ретвитнутое к 'user1' и кладем в перевернутый список.
        for i in range(3):
            tweet = Tweet.objects.create(text=f'tweet{i}', user=self.user2)
            self.user1.retweeted_tweets.add(tweet)
        retweets = reversed(list(self.user1.retweeted_tweets.all()))

        response = self.client.get(reverse('user_profile:profile_tweets', kwargs={'username': self.user1.username}))
        self.assertQuerysetEqual(response.context['object_list'], retweets)

    def test_view_with_user_root_tweets_n_retweets(self):
        '''
        Если у пользователя есть корневые твиты и ретвиты, то отображаети те, и другие 
        по времени совершения действия(время создания твита и время ретвита).
        '''
        # Создаем 4 твита каждым пользователем по очереди и один твит вторым.
        # Твиты 2-ого пользователя, кроме пятого, добавляем в ретвитнутое к 1-му.
        tweet1 = Tweet.objects.create(text='tweet1', user=self.user1)
        tweet2 = Tweet.objects.create(text='tweet2', user=self.user2)
        self.user1.retweeted_tweets.add(tweet2)
        tweet3 = Tweet.objects.create(text='tweet3', user=self.user1)
        tweet4 = Tweet.objects.create(text='tweet4', user=self.user2)
        self.user1.retweeted_tweets.add(tweet4)
        tweet5 = Tweet.objects.create(text='tweet5', user=self.user2)

        response = self.client.get(reverse('user_profile:profile_tweets', kwargs={'username': self.user1.username}))
        self.assertQuerysetEqual(response.context['object_list'], [tweet4, tweet3, tweet2, tweet1])

class ProfileRepliesViewTests(SetUpMixin, TestCase):
    '''Тесты для представления, в котором отображаются только ответы на другие твиты пользователя.'''

    def setUp(self):
        return super().setUp()

    def test_view_url_inaccessible_for_unauthorized(self):
        '''Проверяет, что пользователь не авторизован и переводит его на страницу логина.'''
        response = self.client.get(reverse('user_profile:profile_replies', kwargs={'username': self.user1.username}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/')

    def test_view_url_accessible_by_name(self):
        '''Проверяет, что страница доступна по имени url паттерна.'''
        login = self.login_user1()
        response = self.client.get(reverse('user_profile:profile_replies', kwargs={'username': self.user1.username}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request['PATH_INFO'], '/user1/with_replies/')

    def test_view_uses_correct_template(self):
        '''Проверяет, что представление использует нужный шаблон.'''
        login = self.login_user1()
        response = self.client.get(reverse('user_profile:profile_replies', kwargs={'username': self.user1.username}))
        self.assertTemplateUsed(response, 'user_profile/profile_replies.html')

    def test_view_without_user_replies(self):
        '''Если у пользователя нет ответов на другие твиты, то ничего не отображает.'''
        login = self.login_user1()
        response = self.client.get(reverse('user_profile:profile_replies', kwargs={'username': self.user1.username}))
        self.assertQuerysetEqual(response.context['object_list'], [])

    def test_view_with_user_replies(self):
        '''Если у пользователя есть ответы на другие твиты, то отображает их по времени создания от позднего к раннему.'''
        tweet1 = Tweet.objects.create(text='tweet1', user=self.user1)
        tweet2 = Tweet.objects.create(text='tweet2', user=self.user2)
        tweet3 = Tweet.objects.create(text='reply on tweet1', user=self.user1, parent=tweet1)
        tweet4 = Tweet.objects.create(text='reply on tweet2', user=self.user1, parent=tweet2)
        tweet5 = Tweet.objects.create(text='reply on tweet3', user=self.user1, parent=tweet3)

        login = self.login_user1()
        response = self.client.get(reverse('user_profile:profile_replies', kwargs={'username': self.user1.username}))
        self.assertQuerysetEqual(response.context['object_list'], [tweet5, tweet4, tweet3])

class ProfileLikesViewTests(SetUpMixin, TestCase):
    '''Тесты для представления, в котором отображаются только лайкнутые твиты пользователя.'''

    def setUp(self):
        return super().setUp()

    def test_view_url_inaccessible_for_unauthorized(self):
        '''Проверяет, что пользователь не авторизован и редиректит его на страницу логина.'''
        response = self.client.get(reverse('user_profile:profile_likes', kwargs={'username': self.user1.username}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/')

    def test_view_url_accessible_by_name(self):
        '''Проверяет, что страница доступна по имени url паттерна.'''
        login = self.login_user1()
        response = self.client.get(reverse('user_profile:profile_likes', kwargs={'username': self.user1.username}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request['PATH_INFO'], '/user1/likes/')

    def test_view_uses_correct_template(self):
        '''Проверяет, что представление использует нужный шаблон.'''
        login = self.login_user1()
        response = self.client.get(reverse('user_profile:profile_likes', kwargs={'username': self.user1.username}))
        self.assertTemplateUsed(response, 'user_profile/profile_likes.html')

    def test_view_without_user_likes(self):
        '''Если у пользователя нет лайкнутых твитов, то ничего не отображает.'''
        login = self.login_user1()
        response = self.client.get(reverse('user_profile:profile_likes', kwargs={'username': self.user1.username}))
        self.assertQuerysetEqual(response.context['object_list'], [])

    def test_view_with_user_likes(self):
        '''Если у пользователя есть лайкнутые твиты, то отображает их по времени создания от позднего к раннему.'''
        # Создаем 3 твита и добавлях их в лайкнутое 'user1'
        for i in range(3):
            tweet = Tweet.objects.create(text=f'tweet{i}', user=self.user2)
            self.user1.liked_tweets.add(tweet)
        likes = reversed(list(self.user1.liked_tweets.all()))

        login = self.client.login(username=self.user1, password='Password1')
        response = self.client.get(reverse('user_profile:profile_likes', kwargs={'username': self.user1.username}))
        self.assertQuerysetEqual(response.context['object_list'], likes)

class FollowersViewTests(SetUpMixin, TestCase):
    '''Тесты для представления, в котором отображаются подписчики(читатели) пользователя.'''

    def setUp(self):
        return super().setUp()

    def test_view_url_inaccessible_for_unauthorized(self):
        '''Проверяет, что пользователь не авторизован и редиректит его на страницу логина.'''
        response = self.client.get(reverse('user_profile:user_followers', kwargs={'username': self.user1.username}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/')

    def test_view_url_accessible_by_name(self):
        '''Проверяет, что страница доступна по имени url паттерна.'''
        login = self.login_user1()
        response = self.client.get(reverse('user_profile:user_followers', kwargs={'username': self.user1.username}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request['PATH_INFO'], '/user1/followers/')

    def test_view_uses_correct_template(self):
        '''Проверяет, что представление использует нужный шаблон.'''
        login = self.login_user1()
        response = self.client.get(reverse('user_profile:user_followers', kwargs={'username': self.user1.username}))
        self.assertTemplateUsed(response, 'user_profile/followers.html')

    def test_view_without_followers(self):
        '''Если у пользователя нет подписчиков, то ничего не отображает.'''
        login = self.login_user1()
        response = self.client.get(reverse('user_profile:user_followers', kwargs={'username': self.user1.username}))
        self.assertQuerysetEqual(response.context['object_list'], [])

    def test_view_with_followers(self):
        '''
        Если у пользователя есть подписчики, то отображает их в порядке времени
        от последнего подписавшего до первого подписавшегося.
        '''
        # Создаем 3 пользователя и подписываемся ими на 'user1'
        follower1 = CustomUser.objects.create_user(username='test1', email='test1@test.com', profile_name='test1', password='Password1')
        follower2 = CustomUser.objects.create_user(username='test2', email='test2@test.com', profile_name='test2', password='Password2')
        follower3 = CustomUser.objects.create_user(username='test3', email='test3@test.com', profile_name='test3', password='Password3')
        self.user1.followers.add(follower2)
        self.user1.followers.add(follower3)
        self.user1.followers.add(follower1)
        
        login = self.client.login(username=self.user1, password='Password1')
        response = self.client.get(reverse('user_profile:user_followers', kwargs={'username': self.user1.username}))
        self.assertQuerysetEqual(response.context['object_list'], [follower1, follower3, follower2])

class FollowingViewTests(SetUpMixin, TestCase):
    '''Тесты для представления, в котором отображаются подписки(читаемое) пользователя.'''

    def setUp(self):
        return super().setUp()

    def test_view_url_inaccessible_for_unauthorized(self):
        '''Проверяет, что пользователь не авторизован и редиректит его на страницу логина.'''
        response = self.client.get(reverse('user_profile:user_following', kwargs={'username': self.user1.username}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/')

    def test_view_url_accessible_by_name(self):
        '''Проверяет, что страница доступна по имени url паттерна.'''
        login = self.login_user1()
        response = self.client.get(reverse('user_profile:user_following', kwargs={'username': self.user1.username}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request['PATH_INFO'], '/user1/following/')

    def test_view_uses_correct_template(self):
        '''Проверяет, что представление использует нужный шаблон.'''
        login = self.login_user1()
        response = self.client.get(reverse('user_profile:user_following', kwargs={'username': self.user1.username}))
        self.assertTemplateUsed(response, 'user_profile/followees.html')

    def test_view_without_followees(self):
        '''Если у пользователя нет подписчиков, то ничего не отображает.'''
        login = self.login_user1()
        response = self.client.get(reverse('user_profile:user_following', kwargs={'username': self.user1.username}))
        self.assertQuerysetEqual(response.context['object_list'], [])

    def test_view_with_followees(self):
        '''
        Если у пользователя есть подписки, то отображает их в порядке времени
        от самой недавней подписки до самой первой.
        '''
        # Создаем 3 пользователя и подписываемся на них 'user1'
        followee1 = CustomUser.objects.create_user(username='test1', email='test1@test.com', profile_name='test1', password='Password1')
        followee2 = CustomUser.objects.create_user(username='test2', email='test2@test.com', profile_name='test2', password='Password2')
        followee3 = CustomUser.objects.create_user(username='test3', email='test3@test.com', profile_name='test3', password='Password3')
        self.user1.followees.add(followee3)
        self.user1.followees.add(followee1)
        self.user1.followees.add(followee2)
        
        login = self.client.login(username=self.user1, password='Password1')
        response = self.client.get(reverse('user_profile:user_following', kwargs={'username': self.user1.username}))
        self.assertQuerysetEqual(response.context['object_list'], [followee2, followee1, followee3])

class FollowersYouFollowViewTests(SetUpMixin, TestCase):
    '''
    Тесты для представления, в котором отображаются общие подписчики
    текущего авторизованного пользователя и владельца страницы, на которую он зашел.
    '''

    def setUp(self):
        self.follower1 = CustomUser.objects.create_user(username='test1', email='test1@test.com', profile_name='test1', password='Password1')
        self.follower2 = CustomUser.objects.create_user(username='test2', email='test2@test.com', profile_name='test2', password='Password2')
        self.follower3 = CustomUser.objects.create_user(username='test3', email='test3@test.com', profile_name='test3', password='Password3')
        self.follower4 = CustomUser.objects.create_user(username='test4', email='test4@test.com', profile_name='test4', password='Password4')
        return super().setUp()

    def test_view_url_inaccessible_for_unauthorized(self):
        '''Проверяет, что пользователь не авторизован и редиректит его на страницу логина.'''
        response = self.client.get(reverse('user_profile:followers_you_follow', kwargs={'username': self.user1.username}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/')

    def test_view_url_inaccessible_for_user_himself(self):
        '''
        Проверяет, что текущий авторизованный пользователь не может зайти на запрашиваемую страницу
        у себя же в профиле и его редиректит на страницу с подписчиками(читателями).
        '''
        login = self.login_user1()
        response = self.client.get(reverse('user_profile:followers_you_follow', kwargs={'username': self.user1.username}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/user1/followers/')

    def test_view_url_accessible_by_name(self):
        '''Проверяет, что страница доступна по имени url паттерна в профилях других пользователей.'''
        login = self.login_user1()
        response = self.client.get(reverse('user_profile:followers_you_follow', kwargs={'username': self.user2.username}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request['PATH_INFO'], '/user2/followers_you_follow/')

    def test_view_without_the_same_followers(self):
        '''
        Если у пользователей нет одинаковых подписчиков, то не отображает
        ни соответствующую вкладку, ни общих пользователей.
        '''
        # Добавляем каждому пользователю по подписчику(без одинаковых).
        self.user1.followers.add(self.follower1)
        self.user2.followers.add(self.follower4)

        login = self.login_user1()
        response = self.client.get(reverse('user_profile:followers_you_follow', kwargs={'username': self.user2.username}))
        self.assertQuerysetEqual(response.context['object_list'], [])
        self.assertNotContains(response, 'Читатели, которых вы знаете')

    def test_view_with_the_same_followers(self):
        '''
        Если у пользователей есть общие подписчики, то отображает
        как соответствующую вкладку, так и общих подписчиков в порядке
        добавления в читаемое текущего авторизованного пользователя от
        последнего подписавшегося до первого.
        '''
        # Добавляем каждому пользователю одинаковых подписчиков.
        self.user1.followers.add(self.follower2, self.follower3)
        self.user2.followers.add(self.follower2, self.follower3)

        login = self.login_user1()
        response = self.client.get(reverse('user_profile:followers_you_follow', kwargs={'username': self.user2.username}))
        self.assertQuerysetEqual(response.context['object_list'], [self.follower3, self.follower2])
        self.assertContains(response, 'Читатели, которых вы знаете')

class UserFollowApiViewTests(SetUpMixin, TestCase):
    '''
    Тесты для представления, в котором возвращается JSON
    с подписками(читаемым) текущего авторизованного пользователя.
    '''
    
    def setUp(self):
        return super().setUp()
    
    def test_view_url_accessible_by_name(self):
        '''Проверяет, что страница доступна по имени url паттерна.'''
        response = self.client.get(reverse('user_profile:follow_api'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request['PATH_INFO'], '/follow/api/')

    def test_view_for_unauthorized(self):
        '''Проверяет, что возвращается в JSON для анонимного пользователя.'''
        response = self.client.get(reverse('user_profile:follow_api'))
        self.assertJSONEqual(force_str(response.content), {'user': 'AnonymousUser'})

    def test_view_for_authorized_without_followees(self):
        '''Проверяет, что возвращается в JSON для авторизованного пользователя без подписок.'''
        login = self.login_user1()
        response = self.client.get(reverse('user_profile:follow_api'))
        self.assertJSONEqual(force_str(response.content), {'followees': []})

    def test_view_for_authorized_with_followees(self):
        '''Проверяет, что возвращается в JSON для авторизованного пользователя с подписками.'''
        # Создаем 3 пользователя и подписываемся на них 'user1'
        followee1 = CustomUser.objects.create_user(username='test1', email='test1@test.com', profile_name='test1', password='Password1')
        followee2 = CustomUser.objects.create_user(username='test2', email='test2@test.com', profile_name='test2', password='Password2')
        followee3 = CustomUser.objects.create_user(username='test3', email='test3@test.com', profile_name='test3', password='Password3')
        self.user1.followees.add(followee1, followee2, followee3)

        login = self.login_user1()
        response = self.client.get(reverse('user_profile:follow_api'))
        self.assertJSONEqual(force_str(response.content), {'followees': [followee1.pk, followee2.pk, followee3.pk]})

class FollowUserViewTests(SetUpMixin, TestCase):
    '''
    Тесты для представления, которое обрабатывает добавление пользователя 
    в отслеживаемое(подписки) текущего авторизованного пользователя.
    '''

    def setUp(self):
        return super().setUp()
    
    def test_view_for_unauthorized(self):
        '''
        Проверяет, что сервер отдает 401 ошибку
        и JSON содержит ключ с ошибкой, если пользователь не авторизован.
        '''
        response = self.client.post(
            reverse('user_profile:follow_user'),
            {'user_id': self.user1.pk},
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, 401)
        self.assertIn('error', json_response)

    def test_view_for_authorized_follows_another_user(self):
        '''
        Проверяет, что сервер отдает 200 ответ и соответствующий JSON,
        когда текущий авторизованный пользователь успешно подписался
        на другого пользователя.
        '''
        login = self.login_user1()
        response = self.client.post(
            reverse('user_profile:follow_user'),
            {'user_id': self.user2.pk},
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json_response.get('result', '') == 'followed')
        self.assertIn(self.user2, self.user1.followees.all())

    def test_view_for_authorized_follows_himself(self):
        '''
        Проверяет, что сервер отдает 500 ответ и JSON содержит ключ с ошибкой,
        когда текущий авторизованный пользователь пытается подписаться сам на себя.
        '''
        login = self.login_user1()
        response = self.client.post(
            reverse('user_profile:follow_user'),
            {'user_id': self.user1.pk},
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, 500)
        self.assertIn('error', json_response)

    def test_view_for_authorized_follows_non_existent_user(self):
        '''
        Проверяет, что сервер отдает 500 ответ и JSON содержит ключ с ошибкой,
        когда текущий авторизованный пользователь пытается подписаться на несуществующего пользователя.
        '''
        login = self.login_user1()
        non_existent_pk = CustomUser.objects.last().pk + 1
        response = self.client.post(
            reverse('user_profile:follow_user'),
            {'user_id': non_existent_pk},
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, 500)
        self.assertIn('error', json_response)

class UnfollowUserViewTests(SetUpMixin, TestCase):
    '''
    Тесты для представления, которое обрабатывает удаление пользователя 
    из отслеживаемого(подписок) текущего авторизованного пользователя.
    '''
    
    def setUp(self):
        return super().setUp()

    def test_view_for_unauthorized(self):
        '''
        Проверяет, что сервер отдает 401 ошибку
        и JSON содержит ключ с ошибкой, если пользователь не авторизован.
        '''
        response = self.client.post(
            reverse('user_profile:unfollow_user'),
            {'user_id': self.user1.pk},
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, 401)
        self.assertIn('error', json_response)

    def test_view_for_authorized_unfollows_another_user(self):
        '''
        Проверяет, что сервер отдает 200 ответ и соответствующий JSON,
        когда текущий авторизованный пользователь успешно отписался
        от другого пользователя.
        '''
        self.user1.followees.add(self.user2)
        login = self.login_user1()
        response = self.client.post(
            reverse('user_profile:unfollow_user'),
            {'user_id': self.user2.pk},
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json_response.get('result', '') == 'unfollowed')
        self.assertNotIn(self.user2, self.user1.followees.all())

    def test_view_for_authorized_unfollows_himself(self):
        '''
        Проверяет, что сервер отдает 500 ответ и JSON содержит ключ с ошибкой,
        когда текущий авторизованный пользователь пытается отписаться от самого себя.
        '''
        login = self.login_user1()
        response = self.client.post(
            reverse('user_profile:unfollow_user'),
            {'user_id': self.user1.pk},
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, 500)
        self.assertIn('error', json_response)

    def test_view_for_authorized_unfollows_non_existent_user(self):
        '''
        Проверяет, что сервер отдает 500 ответ и JSON содержит ключ с ошибкой,
        когда текущий авторизованный пользователь пытается отписаться от несуществующего пользователя.
        '''
        login = self.login_user1()
        non_existent_pk = CustomUser.objects.last().pk + 1
        response = self.client.post(
            reverse('user_profile:unfollow_user'),
            {'user_id': non_existent_pk},
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, 500)
        self.assertIn('error', json_response)

class UpdateProfileViewTests(SetUpMixin, TestCase):

    pass
