from django.db import models
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.contrib.postgres.fields import CICharField, CIEmailField

# Create your models here.

def get_profile_photo_path(instance, filename):
    '''Возвращает путь для загрузки фото профиля пользователя.'''
    return f'photos/{instance.username}/{filename}'

class UserFollow(models.Model):
    followee = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='follower_set') # Тот, на кого подписались
    follower = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='followee_set') # Тот, кто подписался
    timestamp = models.DateTimeField(auto_now_add=True)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    '''
        Класс, представляющий кастомную модель таблицы БД пользователя. Для аутентификации по умолчанию используется username.
        Кастомный бекэнд (./auth_backend.py) предоставляет кастомную аутентификацию как по username, так и по email. 
        Для полей с ограничением "unique" используются поля с типом "citext", которые не чувствительны к регистру.
        Следовательно, значения для юзернеймов test, TEST, tEsT и т.д. эквиваленты друг другу.
    '''

    username = CICharField(
        max_length=15,
        unique=True,
        error_messages={'unique': 'Данное имя уже занято. Пожалуйста, выберите другое.'},
        verbose_name='Username'
    )
    email = CIEmailField(
        max_length=255,
        unique=True,
        error_messages={'unique': 'Адрес электронной почты уже занят.'},
        verbose_name='Email'
    )
    profile_name = models.CharField(max_length=50, verbose_name='Имя профиля')
    about = models.CharField(max_length=160, blank=True, verbose_name='О себе')
    location = models.CharField(max_length=30, blank=True, verbose_name='Местоположение')
    website = models.URLField(max_length=100, blank=True, verbose_name='Веб-сайт')
    profile_photo = models.ImageField(upload_to=get_profile_photo_path, blank=True, default=f'photos/default.png/', verbose_name='Фото профиля')
    followers = models.ManyToManyField('self', blank=True, related_name='followees', symmetrical=False, through='UserFollow')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')

    objects = UserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'пользователя'
        verbose_name_plural = 'Пользователи'

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_short_name(self):
        '''Возвращает короткое имя для текущего пользователя, используемое в приветствии в админ панели'''
        return self.username

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''Отправляет email текущему пользователю'''
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_absolute_url(self):
        return reverse('user_profile:profile_tweets', kwargs={'username': self.username})

    def get_profile_photo(self):
        return f'{settings.MEDIA_URL}{self.profile_photo}'

class FooterLinks(models.Model):    
    '''Класс, представляющий модель таблицы БД с ссылками на оригинальную документацию и доп. сервисы твиттера в футере'''

    title = CICharField(max_length=50, unique=True, db_index=False, verbose_name='Заголовок')
    url = models.URLField(unique=True, verbose_name='URL')

    class Meta:
        verbose_name = 'ссылку футера'
        verbose_name_plural = 'Ссылки футера'
        ordering = ('id',)

    def __str__(self):
        return self.title