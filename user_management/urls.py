from django.urls import path
from .views import *
app_name = 'user_management'

urlpatterns = [
    path('register-user', RegisterUser.as_view(), name="register_user"),
    path('login-user', LoginView.as_view(), name="login_user"),
    path('user-information/<slug:query_type>/', UserInformation.as_view(), name="user_information"),
    path('change-password', change_password, name="change_password"),
]