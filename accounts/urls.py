from django.urls import path

from .views import *

urlpatterns = [
    path('signup', UserRegisterView.as_view(), name='signup'),
    # path('login', )
    path('test', TokenTestView.as_view(), name='token-test')
]
