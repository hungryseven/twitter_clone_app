from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

UserModel = get_user_model()

class CustomBackend(ModelBackend):
    '''
        Класс, представляющий кастомный бэкенд, предоставляющий аутентификацию
        как через username, так и через email (не чувствительны к регистру)
    '''

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
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
