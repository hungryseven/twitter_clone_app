from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe

from .models import CustomUser, FooterLinks
from utils.mixins import AdminMixin

# Register your models here.

class UserCreationForm(forms.ModelForm):
    '''
    Форма для создания новых пользователей.
    Включает в себя в необходимые поля + пароль с подтверждением.
    '''
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('username', 'email',)

    def clean_password2(self):
        '''Проверяет совпадение паролей.'''
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Пароли не совпадают")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    '''
    Форма для апдейта информации о пользователе.
    Включает в себя все поля и ридонли поле с кэшем пароля.
    '''
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'profile_name', 'about', 'location', 'website', 'profile_photo', 'is_staff', 'is_active')


class CustomUserAdmin(AdminMixin, BaseUserAdmin):
    '''
    Класс, представляющий админ-панель для модели пользователей.
    '''

    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'email', 'profile_name', 'is_staff')
    list_filter = ('is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'profile_name')
    search_help_text = 'Поиск по имени пользователя, email или имени профиля'
    readonly_fields = (
        'about', 'location', 'get_website_link', 'get_profile_photo', 'date_joined', 'get_followees', 'followees_count', 'get_followers', 'followers_count',
        'get_likes', 'likes_count', 'get_retweets', 'retweets_count', 'get_bookmarks', 'bookmarks_count', 'get_tweets', 'tweets_count'
    )
    show_full_result_count = False
    ordering = ('pk',)
    fieldsets = (
        ('Персональные данные', {
            'fields': ('username', 'email', 'password')
            }
        ),
        ('Персональная информация', {
            'fields': ('profile_name', 'get_profile_photo', 'about', 'location', 'get_website_link', 'date_joined')
            }
        ),
        ('Разрешения', {
            'fields': ('is_staff', 'is_active')
            }
        ),
        ('Твиты', {
            'classes': ('collapse',),
            'fields': ('tweets_count', 'get_tweets'),
            }
        ),
        ('Подписки', {
            'classes': ('collapse',),
            'fields': ('followees_count', 'get_followees'),
            }
        ),
        ('Подписчики', {
            'classes': ('collapse',),
            'fields': ('followers_count', 'get_followers'),
            }
        ),
        ('Лайки', {
            'classes': ('collapse',),
            'fields': ('likes_count', 'get_likes'),
            }
        ),
        ('Ретвиты', {
            'classes': ('collapse',),
            'fields': ('retweets_count', 'get_retweets'),
            }
        ),
        ('Закладки', {
            'classes': ('collapse',),
            'fields': ('bookmarks_count', 'get_bookmarks'),
            }
        ),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'profile_name', 'password1', 'password2'),
            }
        ),
    )

    def get_profile_photo(self, obj):
        '''Отображает фото профиля пользователя.'''
        return mark_safe(f'<img src="{obj.profile_photo.url}" style="object-fit: cover; border-radius: 50%;" width="150" height="150">')

    get_profile_photo.short_description = 'Фото профиля'

    def get_website_link(self, obj):
        '''Возвращает кликабельную ссылку на веб-сайт, если он существует.'''
        if obj.website is not None:
            return mark_safe(f'<a href={obj.website}>{obj.website}</a>')

    get_website_link.short_description = 'Веб-сайт'

    @admin.display(description='Количество твитов')
    def tweets_count(self, obj):
        '''Отображает количество твитов пользователя.'''
        return obj.tweets.count()

    @admin.display(description='Количество подписок')
    def followees_count(self, obj):
        '''Отображает количество подписок пользователя.'''
        return obj.followees.count()

    @admin.display(description='Количество подписчиков')
    def followers_count(self, obj):
        '''Отображает количество подписчиков пользователя.'''
        return obj.followers.count()

    @admin.display(description='Количество лайков')
    def likes_count(self, obj):
        '''Отображает количество лайков пользователя.'''
        return obj.liked_tweets.count()

    @admin.display(description='Количество ретвитов')
    def retweets_count(self, obj):
        '''Отображает количество ретвитов пользователя.'''
        return obj.retweeted_tweets.count()

    @admin.display(description='Количество закладок')
    def bookmarks_count(self, obj):
        '''Отображает количество закладок пользователя.'''
        return obj.bookmarked_tweets.count()

    @admin.display(description='Твиты')
    def get_tweets(self, obj):
        '''Построчно выводит список с твитами пользователя.'''
        return self.get_objects(queryset=obj.tweets.order_by('-pub_date'), line_by_line=True)

    @admin.display(description='Подписки')
    def get_followees(self, obj):
        '''Выводит строку с ссылками на подписки пользователя.'''
        return self.get_objects(queryset=CustomUser.objects.filter(followers=obj).order_by('-follower_set__timestamp'))
    
    @admin.display(description='Подписчики')
    def get_followers(self, obj):
        '''Выводит строку с ссылками на подписчиков пользователя.'''
        return self.get_objects(queryset=CustomUser.objects.filter(followees=obj).order_by('-followee_set__timestamp'))

    @admin.display(description='Лайки')
    def get_likes(self, obj):
        '''Построчно выводит список с лайками пользователя.'''
        return self.get_objects(queryset=obj.liked_tweets.order_by('-tweetlike__timestamp'), line_by_line=True)
    
    @admin.display(description='Ретвиты')
    def get_retweets(self, obj):
        '''Построчно выводит список с ретвитами пользователя.'''
        return self.get_objects(queryset=obj.retweeted_tweets.order_by('-tweetretweet__timestamp'), line_by_line=True)

    @admin.display(description='Закладки')
    def get_bookmarks(self, obj):
        '''Построчно выводит список с закладками пользователя.'''
        return self.get_objects(queryset=obj.bookmarked_tweets.order_by('-tweetbookmark__timestamp'), line_by_line=True)

class FooterLinksAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'url')
    list_display_links = ('id', 'title')
    search_fields = ('title',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(FooterLinks, FooterLinksAdmin)

admin.site.unregister(Group)

admin.site.site_title = 'Twitter'
admin.site.site_header = 'Twitter'
