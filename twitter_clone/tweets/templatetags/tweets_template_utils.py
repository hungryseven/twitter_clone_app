from atexit import register
from django import template
from django.utils.safestring import mark_safe

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
def render_short_tweet(context, tweet):
    '''
        Тэг, который рендерит обычный твит на странице.
    '''

    return {
        'request': context['view'].request,
        'tweet': tweet
    }

@register.inclusion_tag('tweets/tweet_form_snippet.html', takes_context=True)
def render_tweet_form(context, id='', placeholder='Что происходит?'):
    '''
        Тэг, который рендерит форму для создания твитов.
    '''

    return {
        'tweet_form': context['form'],
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