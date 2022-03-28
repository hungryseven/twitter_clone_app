from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

class HomeView(TemplateView):

    template_name = 'main_app/base_main_app.html'