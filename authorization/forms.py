from utils.base_forms import CustomModelForm, CustomForm
from django import forms
from django.forms import TextInput, EmailInput
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
        max_length=15,
        error_messages={
            'min_length': 'Имя пользователя не может быть менее 4 символов.',
            'max_length': 'Имя пользователя не может быть более 15 символов.'
        },
        help_text='Имя пользователя будет использоваться в качестве логина.'
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput()
    )
    password2 = forms.CharField(
        label='Повтор пароля',
        widget=forms.PasswordInput()
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'profile_name', 'password1', 'password2')
        widgets = {
            'username': TextInput,
            'email': EmailInput,
            'profile_name': TextInput
        }
        labels = {
            'username': 'Имя пользователя',
            'email': 'Адрес электронной почты'
        }
        help_texts = {
            'username': 'Имя пользователя будет использоваться в качестве логина.',
        }

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
        widget=forms.TextInput()
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput()
    )
