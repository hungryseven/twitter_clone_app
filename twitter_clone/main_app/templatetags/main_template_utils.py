from django import template

register = template.Library()

@register.filter(name='at')
def add_at_sign(value, arg='@'):
    return arg + value

@register.inclusion_tag('main_app/_right_sidebar_topics.html')
def render_right_sidebar_topics():
    '''Тег рендерит "Актуальные темы" в райтсайд баре.'''
    return

@register.inclusion_tag('main_app/_right_sidebar_users.html')
def render_right_sidebar_users():
    '''Тег рендерит рекомендации для подписки с пользователями в райтсайд баре.'''
    return