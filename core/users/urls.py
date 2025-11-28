from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from api.views import LoginView, LogoutView, RegisterView


app_name = 'users'

urlpatterns = [
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/login/', LoginView.as_view(), name='login_view'),
    path('token/register/', RegisterView.as_view(), name='register_view'),
    path('token/logout/', LogoutView.as_view(), name='logout_view'),
]
