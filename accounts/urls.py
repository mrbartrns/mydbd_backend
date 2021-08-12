from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from .views import *

urlpatterns = [
    path('signup', UserRegisterView.as_view(), name='signup'),
    path('api/login', CustomTokenObtainPairView.as_view(), name='token-login'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token-refresh'),
    path('api/token/verify', TokenVerifyView.as_view(), name='token-verify'),
    path('api/logout', UserLogoutView.as_view(), name='token-logout'),
    path('validate', ValidateSimpleJwtTokenView.as_view(), name='token-validate')
]
