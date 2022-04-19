from django.contrib import admin
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.forms.widgets import Textarea
from mptt.admin import DraggableMPTTAdmin
from .models import Tweet

# Register your models here.

class TweetAdmin(DraggableMPTTAdmin):
    formfield_overrides = {
        models.CharField: {'widget': Textarea(attrs={'rows': 3, 'cols': 60})},
    }

    list_display = ('tree_actions', 'indented_title', 'user', 'pub_date', 'parent')
    list_filter = ('pub_date',)
    list_select_related = ('user', 'parent')
    search_fields = ('text', 'user__username')
    search_help_text = 'Поиск по тексту твита или имени пользователя'
    readonly_fields = ('get_replies', 'replies_count', 'get_likes', 'likes_count', 'get_retweets', 'retweets_count', 'get_bookmarks', 'bookmarks_count')
    show_full_result_count = False
    fieldsets = (
        (None, {
            'fields': ('text', 'user', 'parent'),
        }),
        ('Ответы на текущий твит', {
            'classes': ('collapse',),
            'fields': ('replies_count', 'get_replies'),
        }),
        ('Лайки', {
            'classes': ('collapse',),
            'fields': ('likes_count', 'get_likes'),
        }),
        ('Ретвиты', {
            'classes': ('collapse',),
            'fields': ('retweets_count', 'get_retweets'),
        }),
        ('Закладки', {
            'classes': ('collapse',),
            'fields': ('bookmarks_count', 'get_bookmarks'),
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('likes', 'retweets', 'bookmarks', 'children')

    @admin.display(description='Количество ответов')
    def replies_count(self, obj):
        '''Отображает количество реплаев(ответов) для каждого твита.'''
        return obj.children.count()

    @admin.display(description='Количество лайков')
    def likes_count(self, obj):
        '''Отображает количество лайков для каждого твита.'''
        return obj.likes.count()

    @admin.display(description='Количество ретвитов')
    def retweets_count(self, obj):
        '''Отображает количество ретвитов для каждого твита.'''
        return obj.retweets.count()

    @admin.display(description='Количество закладок')
    def bookmarks_count(self, obj):
        '''Отображает количество закладок для каждого твита.'''
        return obj.bookmarks.count()

    @admin.display(description='Ответы')
    def get_replies(self, obj):
        '''Построчно выводит список ссылок на твиты, которые являются ответом на данный.'''
        replies_list = []
        for children in obj.children.all():
            url = reverse(f'admin:{obj._meta.app_label}_{obj._meta.model_name}_change', args=(children.pk,))
            replies_list.append(f'<p><a href="{url}">{children.text}</a></p>')
        return mark_safe(''.join(replies_list))

    @admin.display(description='Лайкнувшие пользователи')
    def get_likes(self, obj):
        '''Выводит строку с ссылками на пользователей, которые лайкнули текущий твит.'''
        return self.get_users(queryset=obj.likes.all())

    @admin.display(description='Ретвитнувшие пользователи')
    def get_retweets(self, obj):
        '''Выводит строку с ссылками на пользователей, которые ретвитнули текущий твит.'''
        return self.get_users(queryset=obj.retweets.all())

    @admin.display(description='Добавили в закладки')
    def get_bookmarks(self, obj):
        '''Выводит строку с ссылками на пользователей, которые добавили в закладки текущий твит.'''
        return self.get_users(queryset=obj.bookmarks.all())

    @staticmethod
    def get_users(queryset):
        '''Возвращает строку с ссылками на пользователей в админ панели.'''
        users_list = []
        for user in queryset:
            url = reverse(f'admin:{user._meta.app_label}_{user._meta.model_name}_change', args=(user.pk,))
            users_list.append(f'<a href="{url}">{user.username}</a>')
        return mark_safe(', '.join(users_list))

admin.site.register(Tweet, TweetAdmin)


