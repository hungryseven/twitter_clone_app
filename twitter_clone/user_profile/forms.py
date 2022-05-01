from pyexpat import model
from django import forms

from utils.base_forms import CustomModelForm
from authorization.models import CustomUser

class UpdateProfileForm(CustomModelForm):
    '''Класс, представляющий форму для апдейта информации о пользователе.'''

    class Meta:
        model = CustomUser
        fields = ('profile_photo', 'profile_name', 'about', 'location', 'website')
        widgets = {
            'about': forms.Textarea(),
        }