from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.contrib.auth.views import LoginView, LogoutView

from .forms import LoginUserForm, RegisterUserForm
from .models import FooterLinks

from braces.views import AnonymousRequiredMixin

class IndexView(AnonymousRequiredMixin, ListView):
    model = FooterLinks
    template_name = 'authorization/index.html'
    context_object_name = 'links'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Твиттер. Здесь обсуждают все, что происходит.'
        return context

class RegisterUserView(AnonymousRequiredMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'authorization/register.html'
    success_url = reverse_lazy('authorization:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Зарегистрироваться в Твиттере.'
        return context

class LoginUserView(AnonymousRequiredMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'authorization/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Вход в Твиттер.'
        return context

class LogoutUserView(LogoutView):
    pass
