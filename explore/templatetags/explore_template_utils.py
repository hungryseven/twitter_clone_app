from django import template
from django.utils.http import urlencode

register = template.Library()

@register.inclusion_tag('explore/_search_form_snippet.html', takes_context=True)
def render_search_form(context):
    '''Тэг, который рендерит форму поиска.'''
    return {
        'search_form': context['search_form'],
    }

@register.simple_tag
def add_url_params(**kwargs):
    '''Добавляет переданные параметры запроса к URL.'''
    params = {k: v for k, v in kwargs.items() if v is not None}
    if params:
        return f'?{urlencode(params)}'
    return ''