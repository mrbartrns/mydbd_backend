from django.urls import path

from .views import *

urlpatterns = [
    path('', IndexTemplateView.as_view(), name='index')
]
