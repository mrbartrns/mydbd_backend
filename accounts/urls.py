from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from .views import *

urlpatterns = [
    path('signup', UserRegisterView.as_view(), name='signup'),
    path('login', CustomTokenObtainPairView.as_view(), name='token-login'),
    path('token/refresh', TokenRefreshView.as_view(), name='token-refresh'),
    path('token/verify', TokenVerifyView.as_view(), name='token-verify'),
    path('logout', UserLogoutView.as_view(), name='token-logout'),
    path('validate', ValidateSimpleJwtTokenView.as_view(), name='token-validate')
]
