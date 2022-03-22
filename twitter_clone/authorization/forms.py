import re
from twitter_clone.base_forms import CustomForm, CustomModelForm
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

UserModel = get_user_model()

class RegisterUserForm(UserCreationForm, CustomModelForm):

    template_name = 'authorization/form_snippet.html'

    error_messages = {
        'password_mismatch': 'Пароли не совпадают.',
    }
    
    username = forms.CharField(
        label='Имя пользователя',
        min_length=4,
        help_text='Имя пользователя будет использоваться в качестве логина.',
        widget=forms.TextInput(attrs={'class': 'form-control mb-2', 'id': 'floatingUsername', 'placeholder': 'Имя пользователя'})
    )
    email = forms.CharField(
        label='Адрес электронной почты',
        widget=forms.EmailInput(attrs={'class': 'form-control mb-2', 'id': 'floatingEmail', 'placeholder': 'Адрес электронной почты'})
    )
    profile_name = forms.CharField(
        label='Имя профиля',
        widget=forms.TextInput(attrs={'class': 'form-control mb-2', 'id': 'floatingName', 'placeholder': 'Имя'})
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control mb-2', 'id': 'floatingPassword1', 'placeholder': 'Пароль'})
    )
    password2 = forms.CharField(
        label='Повтор пароля',
        widget=forms.PasswordInput(attrs={'class': 'form-control mb-2', 'id': 'floatingPassword2', 'placeholder': 'Повтор пароля'})
    )

    def clean_username(self):
        '''Проверяет соответствие логина/имени пользователя заданному шаблону'''
        username = self.cleaned_data.get('username')
        # Шаблон соответствует строчным и заглавным латинским буквам, цифрам и знаку нижнего подчеркивания
        pattern = re.compile('^[a-zA-Z0-9_]*$')
        result = pattern.findall(username)
        if not result:
            raise ValidationError("Логин может содержать только латинские буквы, цифры и '_'.", code='invalid')
        return username

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'profile_name', 'password1', 'password2')

class LoginUserForm(AuthenticationForm, CustomForm):
    # Переопределяем конструктор, чтобы выставить максимальную длину поля логина в форме 
    # равной максимальной длине email'а, определенной в классе модели юзера (CustomUser),
    # так как с кастомным бэкэндом аутентификации можно логиниться как с username'ом, так и с email'ом
    def __init__(self, request, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.email_field = UserModel._meta.get_field(UserModel.EMAIL_FIELD)
        username_max_length = self.email_field.max_length
        self.fields["username"].max_length = username_max_length
        self.fields["username"].widget.attrs["maxlength"] = username_max_length
        
    template_name = 'authorization/form_snippet.html'

    username = forms.CharField(
        label='Логин или адрес электронной почты',
        widget=forms.TextInput(attrs={'class': 'form-control mb-2', 'id': 'floatingUsername', 'placeholder': 'Логин или адрес электронной почты'})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control mb-2', 'id': 'floatingPassword', 'placeholder': 'Пароль'})
    )
