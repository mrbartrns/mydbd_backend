from django.urls import re_path

from .views import *

urlpatterns = [
    re_path('', IndexTemplateView.as_view(), name='index')
]
