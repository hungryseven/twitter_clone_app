import re
from django import template
from django.utils.safestring import mark_safe

from authorization.models import CustomUser

register = template.Library()

@register.inclusion_tag('tweets/detail_tweet_snippet.html', takes_context=True)
def render_detail_tweet(context, tweet):
    '''
    Тэг, который рендерит главный/детальный твит на странице.
    '''
    return {
        'request': context['view'].request,
        'detail_tweet': tweet
    }

@register.inclusion_tag('tweets/short_tweet_snippet.html', takes_context=True)
def render_short_tweet(context, tweet, is_retweet=False):
    '''
    Тэг, который рендерит обычный твит на странице.

    param:
            is_retweet: если данный параметр установлен в True, то тэг рендерит куски кода с информацией о том,
                        что данный твит был ретвитнут текущим пользователем(на странице профиля).
    '''
    return {
        'request': context['view'].request,
        'tweet': tweet,
        'is_retweet': is_retweet
    }

@register.inclusion_tag('tweets/tweet_form_snippet.html', takes_context=True)
def render_tweet_form(context, id='', placeholder='Что происходит?'):
    '''
    Тэг, который рендерит форму для создания твитов.
    '''
    return {
        'request': context['view'].request,
        'tweet_form': context['tweet_form'],
        'id': id,
        'placeholder': placeholder
    }

@register.filter
def is_zero(value):
    '''
    Фильтр, предназначенный для отображения количества реплаев, ретвитов и лайков.
    Если оно равно 0, то значение заменяется пустой строкой.
    '''
    return '' if value == 0 else value

@register.simple_tag
def replace_usernames_with_links(text, tweet):
    '''
    Тэг заменяет все существующие юзернеймы пользователей,
    которые начинаются с символа "@" и находятся в тексте твита,
    на соответствующие ссылки на страницы профилей этих пользователей.
    '''
    mentioned_users = tweet.mentioned_users.all()
    for user in mentioned_users:
        
        # Достаем юзернейм пользователя из текста в оригинальном виде,
        # так как он может быть написан буквами разных регистров.
        username_in_text = re.search(user.username, text, re.IGNORECASE).group()
        text = re.sub(
            rf'@\b{username_in_text}\b',
            f'<a href="{user.get_absolute_url()}" class="username-link">@{username_in_text}</a>',
            text,
            flags=re.IGNORECASE
        )
    return mark_safe(text)