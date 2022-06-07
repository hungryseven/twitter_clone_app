from django import forms

from utils.base_forms import CustomModelForm
from .models import Tweet

class TweetForm(CustomModelForm):
    '''Класс, представляющий форму для создания твитов.'''
    
    parent = forms.IntegerField(
        required=False,
        widget=forms.HiddenInput
    )
    
    class Meta:
        model = Tweet
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(),
        }