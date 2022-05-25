from django import forms

from utils.base_forms import CustomForm

class SearchForm(CustomForm):
    '''Форма с полем для поиска.'''
    
    q = forms.CharField(
        label='Поисковой запрос',
        required=True,
        error_messages={
            'required': 'Поисковой запрос не может быть пустым.'
        },
        widget=forms.TextInput(),
    )
    f = forms.CharField(
        label='Тип запроса',
        widget=forms.TextInput()
    )