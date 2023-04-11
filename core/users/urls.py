from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path("register/", Register.as_view(), name="register"),
    path("login/", Login.as_view(), name="login"),
    path("logout/", Logout.as_view(), name="logout"),
    path("profile/", ProfileDetailAPI.as_view(), name="profile"),
    path("refresh-token-payload/", TokenRefreshView.as_view(), name="token_refresh2"),
    path('view-cart/', ViewCartAPI.as_view(), name='view-cart'),
]