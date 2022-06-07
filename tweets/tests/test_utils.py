import re
from django.test import TestCase

from tweets.models import filter_tweet_text

class UtilsTest(TestCase):

    def test_filter_func(self):
        '''Тест для фильтра юзернеймов и тегов в тексте твита.'''
        text = 'Текст для теста @username @user @test_user @username @user1 \
                not@username #tag #tag_1 #2tag #tag not#tag3 @!#tag4'
        filtered_text = filter_tweet_text(text)
        self.assertEqual(
            filtered_text,
            ['@username', '@user', '@test_user', '@user1', '#tag', '#tag_1', '#2tag', '#tag4']
        )

    def test_tags_regex(self):
        '''Тест регулярного выражения для поиска тегов в тексте твита.'''
        text = '#tag1 #_tag2 #3tag #_4tag #tag5_ #tag6#not_a_tag #tag7! #tag8? @!$#tag9 \
                #tag10@#tag11 #тег12 ###tag13 not_a_tag#tag14'
        pattern = r'(^|\B)#(?![0-9_]+\b)([a-zA-Zа-яА-ЯёЁ0-9_]+)(\b|\r)'
        matches = []
        for tag in text.split():
            possible_tag = re.search(pattern, tag)
            if possible_tag:
                matches.append(possible_tag.group())
        self.assertEqual(
            matches,
            ['#tag1', '#_tag2', '#3tag', '#_4tag', '#tag5_', '#tag6', '#tag7', '#tag8', '#tag9', '#tag10', '#тег12', '#tag13'] 
        )

    def test_usernames_regex(self):
        '''Тест регулярного выражения для поиска юзернеймов в тексте твита.'''
        text = '@username @username1 @user_name2 @_username3 @longlonglongusername4 @username5@username5 \
                @username6!@username6 not@username7 @username8!?#%^& @username9!&*()@'
        pattern = r'(?<!\S)@(\w{4,15})\b(?!.*@)'
        matches = []
        for username in text.split():
            possible_username = re.search(pattern, username)
            if possible_username:
                matches.append(possible_username.group())
        self.assertEqual(
            matches,
            ['@username', '@username1', '@user_name2', '@_username3', '@username8'] 
        )
