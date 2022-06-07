from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ValidationError
from django.db.models import Q

UserModel = get_user_model()

class CustomBackend(ModelBackend):
    '''
    Класс, представляющий кастомный бэкенд, предоставляющий аутентификацию
    как через username, так и через email (не чувствительны к регистру)
    '''

    error_messages = {
        'wrong_password': 'Неправильный пароль',
        'user_doesnt_exist': 'Мы не смогли найти вашу учетную запись.'
    }

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        if username is None or password is None:
            return
        try:
            # Запрос для поиска пользователя в БД по username или email
            user = UserModel.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
            else:
                raise self.get_wrong_password_error()
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
            raise self.get_user_doesnt_exist_error()

    def get_wrong_password_error(self):
        return ValidationError(
                self.error_messages['wrong_password'],
                code='wrong_password'
            )

    def get_user_doesnt_exist_error(self):
        return ValidationError(
                self.error_messages['user_doesnt_exist'],
                code='user_doesnt_exist'
            )
