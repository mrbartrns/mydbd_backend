from django.urls import path

from .views import *

urlpatterns = [
    path('signup', UserRegisterView.as_view(), name='signup'),
]
