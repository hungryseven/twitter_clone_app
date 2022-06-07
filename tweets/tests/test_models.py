from django.test import TestCase

from authorization.models import CustomUser
from tweets.models import Tweet, Tag

class SetUpMixin:

    def setUp(self):
        self.user1 = CustomUser.objects.create_user(username='user1', email='user1@test.com', profile_name='user1', password='Password1')
        self.user2 = CustomUser.objects.create_user(username='user2', email='user2@test.com', profile_name='user2', password='Password2')
        self.user3 = CustomUser.objects.create_user(username='user3', email='user3@test.com', profile_name='user3', password='Password3')

class TweetModelTest(SetUpMixin, TestCase):
    '''Тесты для модели Tweet.'''

    def test_get_absolute_url(self):
        '''Тест метода "get_absolute_url".'''
        tweet = Tweet.objects.create(text='text', user=self.user1)
        url = tweet.get_absolute_url()
        self.assertEqual(url, f'/user1/status/{tweet.pk}/')

    def test_save_with_usernames_only(self):
        '''Тест метода "save", если в тексте твита только юзернеймы.'''
        tweet = Tweet.objects.create(text='Уведомления для @user1 @user2 @user3 @user4', user=self.user1)
        mentioned_users = tweet.mentioned_users.all()
        self.assertQuerysetEqual(mentioned_users, [self.user1, self.user2, self.user3], ordered=False)

    def test_save_with_tags_only(self):
        '''Тест метода "save", если в тексте твита только теги.'''
        tweet = Tweet.objects.create(
            text='Пишу теги: #tag1 #_tag2 #3tag #tag_4 #5_tag #tag6#tag #tag7!&*^? @!$#tag8 \
                    not#tag9 #tag10@#tag11 #тег12',
            user=self.user1
        )
        tags = [tag.tag_name for tag in tweet.related_tags.all()]
        self.assertEqual(len(tags), 10)
        self.assertEqual(
            tags,
            ['#tag1', '#_tag2', '#3tag', '#tag_4', '#5_tag', '#tag6', '#tag7', '#tag8', '#tag10', '#тег12']
        )

    def test_save_with_tags_n_usernames(self):
        '''Тест метода "save", если в тексте твита и юзернеймы, и теги.'''
        tweet = Tweet.objects.create(
            text='Тест метода @username @user1! @user3? @user2))) @test_user \
                    #testing #tweet #тест не#тег @!#_one_more_tag!!!!',
            user=self.user1
        )
        mentioned_users = tweet.mentioned_users.all()
        self.assertQuerysetEqual(mentioned_users, [self.user1, self.user3, self.user2], ordered=False)

        tags = [tag.tag_name for tag in tweet.related_tags.all()]
        self.assertEqual(len(tags), 4)
        self.assertEqual(
            tags,
            ['#testing', '#tweet', '#тест', '#_one_more_tag'],
        )

class TagModelTest(TestCase):
    '''Тесты для модели Tag.'''

    def test_get_absolute_url(self):
        '''Тест метода "get_absolute_url".'''
        tag = Tag.objects.create(tag_name='#tag')
        url = tag.get_absolute_url()
        self.assertEqual(url, '/search/?q=%23tag&f=')