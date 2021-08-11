from django.views.generic.base import TemplateView


# Create your views here.
class IndexTemplateView(TemplateView):
    template_name = 'frontend/index.html'
