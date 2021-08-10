from django.urls import path

from .views import *

urlpatterns = [
    path('signup', UserRegisterView.as_view(), name='signup'),
    path('validate', ValidateJwtTokenView.as_view(), name='validate-token'),
]
