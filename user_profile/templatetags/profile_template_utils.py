from django import template

register = template.Library()

@register.inclusion_tag('user_profile/_profile_navbar_snippet.html')
def render_profile_navbar(profile_owner):
    '''Рендерит навигационную панель на странице профиля.'''
    return {
        'profile_owner': profile_owner
    }

@register.inclusion_tag('user_profile/_user_info_snippet.html', takes_context=True)
def render_user_info(context, profile_owner, current_user):
    '''Рендерит информацию о пользователе в профиле.'''
    var_dict = {
        'profile_owner': profile_owner,
        'current_user': current_user
    }
    if current_user.is_authenticated:
        var_dict.update(familiar_followers=context['familiar_followers'])
    return var_dict

@register.inclusion_tag('user_profile/_profile_header_snippet.html', takes_context=True)
def render_profile_header(context, profile_owner, current_user):
    '''Рендерит хедер в профиле пользователя(фотография, кнопки с действиями и т.д.).'''
    var_dict = {
        'profile_owner': profile_owner,
        'current_user': current_user
    }
    if current_user.is_authenticated:
        var_dict.update(profile_form=context['profile_form'])
    return var_dict

@register.inclusion_tag('user_profile/_update_form_modal_snippet.html')
def render_profile_modal(current_user, profile_form):
    '''Рендерит модальное окно с формой апдейта профиля пользователя.'''
    return {
        'profile_form': profile_form,
        'current_user': current_user
    }

@register.inclusion_tag('user_profile/_user_card_snippet.html')
def render_user_card(user, current_user):
    '''Рендерит карточку пользователя на страницах подписчиков и подписок.'''
    return {
        'user': user,
        'current_user': current_user
    }

@register.inclusion_tag('user_profile/_is_follow_you_snippet.html')
def is_follow_you(user, current_user):
    '''Рендерит подсказку о том, подписан ли данный пользователь на текущего пользователя.'''
    return {
        'user': user,
        'current_user': current_user
    }



