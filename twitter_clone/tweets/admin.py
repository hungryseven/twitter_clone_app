from django.contrib import admin
from django.db import models
from django.forms.widgets import Textarea

from mptt.admin import DraggableMPTTAdmin

from .models import Tweet
from utils.mixins import AdminMixin

# Register your models here.

class TweetAdmin(AdminMixin, DraggableMPTTAdmin):
    '''
    Класс, представляющий админ-панель для модели твитов.
    '''

    formfield_overrides = {
        models.CharField: {'widget': Textarea(attrs={'rows': 10, 'cols': 60})},
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
            }
        ),
        ('Ответы на текущий твит', {
            'classes': ('collapse',),
            'fields': ('replies_count', 'get_replies'),
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
        return self.get_objects(queryset=obj.children.all(), line_by_line=True)

    @admin.display(description='Лайкнувшие пользователи')
    def get_likes(self, obj):
        '''Выводит строку с ссылками на пользователей, которые лайкнули текущий твит.'''
        return self.get_objects(queryset=obj.likes.order_by('-tweetlike__timestamp'))

    @admin.display(description='Ретвитнувшие пользователи')
    def get_retweets(self, obj):
        '''Выводит строку с ссылками на пользователей, которые ретвитнули текущий твит.'''
        return self.get_objects(queryset=obj.retweets.order_by('-tweetretweet__timestamp'))

    @admin.display(description='Добавили в закладки')
    def get_bookmarks(self, obj):
        '''Выводит строку с ссылками на пользователей, которые добавили в закладки текущий твит.'''
        return self.get_objects(queryset=obj.bookmarks.order_by('-tweetbookmark__timestamp'))

admin.site.register(Tweet, TweetAdmin)