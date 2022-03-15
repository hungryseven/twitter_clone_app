from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, UserManager

# Create your models here.

class CustomUser(AbstractBaseUser, PermissionsMixin):
    '''
        Класс, представляющий кастомную модель пользователя.
        Для аутентификации используется username.
    '''

    username = models.CharField(max_length=15, unique=True, verbose_name='Username')
    email = models.EmailField(max_length=255, unique=True, verbose_name='Email')
    profile_name = models.CharField(max_length=50, blank=True, verbose_name='Имя профиля')
    about = models.CharField(max_length=160, blank=True, verbose_name='О себе')
    location = models.CharField(max_length=30, blank=True, verbose_name='Местоположение')
    website = models.URLField(max_length=100, blank=True, verbose_name='Веб-сайт')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')

    objects = UserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_short_name(self):
        '''Возвращает короткое имя для текущего пользователя, используемое в приветствии в админ панели'''
        return self.username

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''Отправляет email текущему пользователю'''
        send_mail(subject, message, from_email, [self.email], **kwargs)


class FooterLinks(models.Model):    
    '''Класс FooterLinks предоставляет ссылки на оригинальную документацию и доп. сервисы твиттера в футере'''

    title = models.CharField(max_length=50, unique=True, verbose_name='Заголовок')
    url = models.URLField(unique=True, verbose_name='URL')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Footer links'
        verbose_name_plural = 'Footer links'
        ordering = ['id']