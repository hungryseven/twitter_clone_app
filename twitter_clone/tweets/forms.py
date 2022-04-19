from django import forms
from twitter_clone.base_forms import CustomModelForm

from .models import Tweet

class TweetForm(CustomModelForm):
    parent = forms.IntegerField(
        required=False,
        widget=forms.HiddenInput
    )
    text = forms.CharField(
        widget=forms.Textarea
    )
    
    class Meta:
        model = Tweet
        fields = ('text',)