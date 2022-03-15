from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import CustomUser, FooterLinks

# Register your models here.

class UserCreationForm(forms.ModelForm):
    """
        Форма для создания новых пользователей.
        Включает в себя в необходимые поля + пароль с подтверждением.
    """
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('username', 'email')

    def clean_password2(self):
        # Проверка совпадения паролей
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Пароли не совпадают")
        return password2

    def save(self, commit=True):
        # Кэшируем и сохраняем пароль
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    '''
        Форма для апдейта информации о пользователе.
        Включает в себя все поля и ридонли поле с кэшем пароля.
    '''
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'profile_name', 'about', 'location', 'website', 'is_staff', 'is_active')


class CustomUserAdmin(BaseUserAdmin):
    # Формы для создания и апдейта пользователей
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('id', 'username', 'email', 'profile_name', 'about', 'location', 'website', 'is_staff', 'is_active')
    readonly_fields = ('date_joined', )
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        ('Персональные данные', {'fields': ('username', 'email', 'password')}),
        ('Персональная информация', {'fields': ('profile_name', 'about', 'location', 'website', 'date_joined')}),
        ('Разрешения', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    search_fields = ('username', 'email', 'profile_name')
    ordering = ('id',)
    filter_horizontal = ()

class FooterLinksAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'url')
    list_display_links = ('id', 'title')
    search_fields = ('title',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(FooterLinks, FooterLinksAdmin)

admin.site.unregister(Group)

admin.site.site_title = 'Twitter'
admin.site.site_header = 'Twitter'
