from django.shortcuts import render
from django.views.generic import ListView, CreateView

from .models import FooterLinks

# Create your views here.

class IndexView(ListView):
    model = FooterLinks
    template_name = 'authorization/index.html'
    context_object_name = 'links'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Твиттер. Здесь обсуждают все, что происходит.'
        return context

class RegisterView(CreateView):
    template_name = 'authorization/register.html'

