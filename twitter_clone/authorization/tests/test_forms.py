from django.test import TestCase
from django.urls import reverse

from authorization.forms import LoginUserForm, RegisterUserForm
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

class RegisterUserFormTest(setUpTestDataMixin, TestCase):
    '''Тесты для формы регистрации пользователей.'''
    
    def test_form_valid_data(self):
        '''Тест формы с валидными данными.'''
        form = RegisterUserForm(data={
            'username': 'username',
            'email': 'username@test.com',
            'profile_name': 'username',
            'password1': 'SuperSecret1',
            'password2': 'SuperSecret1'
        })
        self.assertTrue(form.is_valid())

    def test_blank_form(self):
        '''Тест формы с пустыми полями.'''
        form = RegisterUserForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 5)

    def test_username_field_constraints(self):
        '''Тест ограничений для поля "username".'''
        form = RegisterUserForm()
        self.assertEqual(form.fields['username'].max_length, 15)
        self.assertEqual(form.fields['username'].min_length, 4)

    def test_form_with_existing_username(self):
        '''Тест формы с существующим именем пользователя.'''
        form = RegisterUserForm(data={
            'username': 'user1',
            'email': 'username@test.com',
            'profile_name': 'test_user',
            'password1': 'SuperSecret1',
            'password2': 'SuperSecret1'
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'], ['Данное имя уже занято. Пожалуйста, выберите другое.'])

    def test_form_with_existing_email(self):
        '''Тест формы с существующим адресом электронной почты.'''
        form = RegisterUserForm(data={
            'username': 'username',
            'email': 'user1@test.com',
            'profile_name': 'test_user',
            'password1': 'SuperSecret1',
            'password2': 'SuperSecret1'
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], ['Адрес электронной почты уже занят.'])

    def test_form_with_username_less_than_4_chars(self):
        '''Тест формы с введенным именем пользователя менее 4 символов.'''
        form = RegisterUserForm(data={
            'username': 'usr',
            'email': 'username@test.com',
            'profile_name': 'test_user',
            'password1': 'SuperSecret1',
            'password2': 'SuperSecret1'
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'], ['Имя пользователя не может быть менее 4 символов.'])

    def test_form_with_username_more_than_15_chars(self):
        '''Тест формы с введенным именем пользователя более 15 символов.'''
        form = RegisterUserForm(data={
            'username': 'verylonguserusername',
            'email': 'username@test.com',
            'profile_name': 'test_user',
            'password1': 'SuperSecret1',
            'password2': 'SuperSecret1'
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'], ['Имя пользователя не может быть более 15 символов.'])

    def test_form_with_invalid_username(self):
        '''Тест формы с невалидным именем пользователя.'''
        form = RegisterUserForm(data={
            'username': 'юзернейм',
            'email': 'username@test.com',
            'profile_name': 'test_user',
            'password1': 'SuperSecret1',
            'password2': 'SuperSecret1'
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'], ["Имя пользователя может содержать только латинские буквы, цифры и '_'."])

    def test_form_with_different_passwords(self):
        '''Тест формы с несовпадающими паролями.'''
        form = RegisterUserForm(data={
            'username': 'username',
            'email': 'username@test.com',
            'profile_name': 'test_user',
            'password1': 'SuperSecret1',
            'password2': 'SuperSecret2'
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password2'], ['Пароли не совпадают.'])

class LoginUserFormTest(setUpTestDataMixin, TestCase):
    '''Тесты для формы авторизации пользователей.'''

    def test_form_valid_data(self):
        '''Тест формы с валидными данными.'''
        response = self.client.get(reverse('authorization:login'))
        form = LoginUserForm(response.request, data={'username': 'user1', 'password': 'SuperSecret1'})
        self.assertTrue(form.is_valid())

    def test_blank_form(self):
        '''Тест формы с пустыми полями.'''
        response = self.client.get(reverse('authorization:login'))
        form = LoginUserForm(response.request, data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)

    def test_username_field_constraints(self):
        '''Тест ограничений для поля "username".'''
        response = self.client.get(reverse('authorization:login'))
        form = LoginUserForm(response.request)
        self.assertEqual(form.fields['username'].max_length, 255)

    def test_form_for_non_existent_user_login_with_username(self):
        '''Тест для формы, если в поле логина введен несуществующий юзернейм.'''
        response = self.client.get(reverse('authorization:login'))
        form = LoginUserForm(response.request, data={'username': 'non_existent', 'password': 'SuperSecret1'})
        self.assertEqual(form.non_field_errors(), ['Мы не смогли найти вашу учетную запись.'])
        self.assertFalse(form.is_valid())

    def test_form_for_non_existent_user_login_with_email(self):
        '''Тест для формы, если в поле логина введена несуществующая почта.'''
        response = self.client.get(reverse('authorization:login'))
        form = LoginUserForm(response.request, data={'username': 'non_existent@mail.com', 'password': 'SuperSecret1'})
        self.assertEqual(form.non_field_errors(), ['Мы не смогли найти вашу учетную запись.'])
        self.assertFalse(form.is_valid())

    def test_form_with_wrong_user_password(self):
        '''Тест для формы, если в поле пользователь ввел неправильный пароль.'''
        response = self.client.get(reverse('authorization:login'))
        form = LoginUserForm(response.request, data={'username': 'user1', 'password': 'WrongPassword'})
        self.assertEqual(form.non_field_errors(), ['Неправильный пароль'])
        self.assertFalse(form.is_valid())