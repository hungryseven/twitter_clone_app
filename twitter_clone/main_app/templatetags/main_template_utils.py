from django import template

register = template.Library()

@register.filter(name='at')
def add_at_sign(value, arg='@'):
    return arg + value