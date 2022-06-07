from django.test import TestCase

from authorization.models import CustomUser

class CustomUserTest(TestCase):
    '''Тесты для модели, представляющей пользователей.'''
    
    @classmethod
    def setUpTestData(cls):
        cls.user1= CustomUser.objects.create_user(
            username='user1',
            email='user1@test.com',
            profile_name='user1', 
            password='Password1'
        )

    def test_username_field_constraints(self):
        '''Тест ограничений для поля "username".'''
        max_length = self.user1._meta.get_field('username').max_length
        self.assertEqual(max_length, 15)

    def test_email_field_constraints(self):
        '''Тест ограничений для поля "email".'''
        max_length = self.user1._meta.get_field('email').max_length
        self.assertEqual(max_length, 255)

    def test_profile_name_field_constraints(self):
        '''Тест ограничений для поля "profile_name".'''
        max_length = self.user1._meta.get_field('profile_name').max_length
        self.assertEqual(max_length, 50)

    def test_about_field_constraints(self):
        '''Тест ограничений для поля "about".'''
        max_length = self.user1._meta.get_field('about').max_length
        self.assertEqual(max_length, 160)

    def test_location_field_constraints(self):
        '''Тест ограничений для поля "location".'''
        max_length = self.user1._meta.get_field('location').max_length
        self.assertEqual(max_length, 30)

    def test_website_field_constraints(self):
        '''Тест ограничений для поля "website".'''
        max_length = self.user1._meta.get_field('website').max_length
        self.assertEqual(max_length, 100)

    def test_profile_photo_field_upload_path(self):
        '''Тест пути загрузки фотографии профиля пользователя.'''
        path = self.user1._meta.get_field('profile_photo').upload_to(self.user, 'profile_photo')
        self.assertEqual(path, 'photos/user1/profile_photo')

    def test_get_absolute_url(self):
        '''Тест метода "get_absolute_url".'''
        url = self.user1.get_absolute_url()
        self.assertEquals(url, '/user1/')