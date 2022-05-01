from django.views.generic import TemplateView

from utils.mixins import DataMixin

# Create your views here.

class HomeView(DataMixin, TemplateView):

    template_name = 'main_app/base_main_app.html'