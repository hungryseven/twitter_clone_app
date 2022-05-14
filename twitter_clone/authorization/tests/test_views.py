from urllib import response
from django.test import TestCase
from django.urls import reverse

from authorization.models import CustomUser

class setUpTestDataMixin:

    @classmethod
    def setUpTestData(cls):
        cls.user1 = CustomUser.objects.create_user(
            username='user1',
            email='user1@test.com',
            profile_name='user1', 
            password='SuperSecret1'
        )

class IndexViewTest(setUpTestDataMixin, TestCase):
    '''Тесты для представления с главной страницей.'''

    def test_view_url_accessible_by_name(self):
        '''Проверяет, что страница доступна по имени url паттерна.'''
        response = self.client.get(reverse('authorization:index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request['PATH_INFO'], '/')

    def test_view_uses_correct_template(self):
        '''Проверяет, что представление использует нужный шаблон.'''
        response = self.client.get(reverse('authorization:index'))
        self.assertTemplateUsed(response, 'authorization/index.html')

    def test_view_inaccessible_for_authorized(self):
        '''Проверяет, что пользователь авторизован и редиректит его на домашнюю страницу.'''
        login = self.client.login(username='user1', password='SuperSecret1')
        response = self.client.get(reverse('authorization:index'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/home/')


class RegisterUserViewTest(setUpTestDataMixin, TestCase):
    '''Тесты для представления с формой регистрацией пользователей.'''

    def test_view_url_accessible_by_name(self):
        '''Проверяет, что страница доступна по имени url паттерна.'''
        response = self.client.get(reverse('authorization:register'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request['PATH_INFO'], '/register/')

    def test_view_uses_correct_template(self):
        '''Проверяет, что представление использует нужный шаблон.'''
        response = self.client.get(reverse('authorization:register'))
        self.assertTemplateUsed(response, 'authorization/register.html')

    def test_view_inaccessible_for_authorized(self):
        '''Проверяет, что пользователь авторизован и редиректит его на домашнюю страницу.'''
        login = self.client.login(username='user1', password='SuperSecret1')
        response = self.client.get(reverse('authorization:register'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/home/')

    def test_view_with_valid_form_data(self):
        '''Проверяет, что при успешной регистрации пользователя редиректит на страницу логина.'''
        response = self.client.post(
            reverse('authorization:register'),
            {
                'username': 'user2',
                'email': 'user2@test.com',
                'profile_name': 'user2', 
                'password1': 'SuperSecret2',
                'password2': 'SuperSecret2'
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/')

class LoginUserViewTest(setUpTestDataMixin, TestCase):
    '''Тесты для представления с формой авторизации пользователей.'''

    def test_view_url_accessible_by_name(self):
        '''Проверяет, что страница доступна по имени url паттерна.'''
        response = self.client.get(reverse('authorization:login'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request['PATH_INFO'], '/login/')

    def test_view_uses_correct_template(self):
        '''Проверяет, что представление использует нужный шаблон.'''
        response = self.client.get(reverse('authorization:login'))
        self.assertTemplateUsed(response, 'authorization/login.html')

    def test_view_inaccessible_for_authorized(self):
        '''Проверяет, что пользователь авторизован и редиректит его на домашнюю страницу.'''
        login = self.client.login(username='user1', password='SuperSecret1')
        response = self.client.get(reverse('authorization:login'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/home/')

    def test_authorization_with_username(self):
        '''Проверяет, что при успешном логине через юзернейм пользователя редиректит на главную(домашнюю) страницу.'''
        response = self.client.post(
            reverse('authorization:login'),
            {
                'username': 'user1',
                'password': 'SuperSecret1',
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/home/')

    def test_authorization_with_email(self):
        '''Проверяет, что при успешном логине через почту пользователя редиректит на домашнюю страницу.'''
        response = self.client.post(
            reverse('authorization:login'),
            {
                'username': 'user1@test.com',
                'password': 'SuperSecret1',
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/home/')


class LogoutUserViewTest(setUpTestDataMixin, TestCase):
    '''Тесты для представления с логаутом пользователей.'''

    def test_logout(self):
        '''Проверяет, что авторизованный пользователь успешно выходит из профиля.'''
        login = self.client.login(username='user1', password='SuperSecret1')
        response = self.client.post(reverse('authorization:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')