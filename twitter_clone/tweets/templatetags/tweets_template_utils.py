import re
from django import template
from django.utils.safestring import mark_safe

from itertools import chain

register = template.Library()

@register.inclusion_tag('tweets/detail_tweet_snippet.html', takes_context=True)
def render_detail_tweet(context, tweet):
    '''Тэг, который рендерит главный/детальный твит на странице.'''
    return {
        'request': context['view'].request,
        'detail_tweet': tweet
    }

@register.inclusion_tag('tweets/short_tweet_snippet.html', takes_context=True)
def render_short_tweet(context, tweet):
    '''
    Тэг, который рендерит обычный твит на странице.
    '''
    var_dict = {
        'request': context['view'].request,
        'tweet': tweet,
    }
    # Если данный твит является ретвитом, то получаем id пользователя,
    # который его ретвитнул. Если в запросе нет такой колонки,
    # то перехватываем ошибку.
    try:
        retweeted_by = tweet.retweeted_by
    except AttributeError:
        return var_dict

    # Если полученный id пользователя отличен от 0.
    if retweeted_by:
        # print(tweet.retweets.filter(pk=retweeted_by).get())
        # print(tweet.retweets.get(pk=retweeted_by))
        for user in tweet.retweets.all():
            if user.pk == retweeted_by:
                retweeted_user = user
        var_dict.update(retweeted_user=retweeted_user)
    return var_dict

@register.inclusion_tag('tweets/tweet_form_snippet.html', takes_context=True)
def render_tweet_form(context, id='', placeholder='Что происходит?', submit_value='Твитнуть'):
    '''Тэг, который рендерит форму для создания твитов.'''
    return {
        'request': context['view'].request,
        'tweet_form': context['tweet_form'],
        'id': id,
        'placeholder': placeholder,
        'submit_value': submit_value
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
    Тег заменяет все юзернеймы пользователей, начинающиеся с символа "@",
    если они существуют, и теги в тексте твита на ссылки на страницы
    профилей и страницу поиска соответственно.
    '''
    mentioned_users = tweet.mentioned_users.all()
    related_tags = tweet.related_tags.all()

    # Объединем два qs в общий список.
    objects_to_link = list(chain(mentioned_users, related_tags))

    # Проходимся по списку и заменяем текущий объект на ссылку.
    for object in objects_to_link:
        if hasattr(object, 'username'):
            object_name = f'@{object.username}'
        else:
            object_name = object.tag_name

        # Т.к. юзернеймы и теги не чувствительны к регистру,
        # сначала находим оригинальное написание объекта в тексте.
        object_in_text = re.search(rf'{object_name}', text, re.IGNORECASE).group()
        
        text = re.sub(
            rf'{object_name}\b',
            f'<a href="{object.get_absolute_url()}" class="linked_text">{object_in_text}</a>',
            text,
            flags=re.IGNORECASE
        )
    return mark_safe(text)