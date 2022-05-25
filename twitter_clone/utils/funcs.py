from django.urls import reverse
from django.utils.http import urlencode

def build_url(*args, **kwargs):
    '''Возвращает url с get параметрами, если они есть.'''
    get_params = kwargs.pop('get', {})
    url = reverse(*args, **kwargs)
    if get_params:
        url += '?' + urlencode(get_params)
    return url