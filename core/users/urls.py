from django.urls import path
from .views import *


urlpatterns = [
    path("register/", Register.as_view(), name="register"),
    path("login/", Login.as_view(), name="login"),
    path("profile/", ProfileDetailAPI.as_view(), name="profile"),
    path('view-cart/', ViewCartAPI.as_view(), name='view-cart'),
    path('update-cart/', UpdateCartAPI.as_view(), name='update-cart'),
    path('update-user/', UpdateUserAPI.as_view(), name='update-user'),
    path('update-customer/', UpdateCustomerAPI.as_view(), name='update-customer'),
    path('update-seller/', UpdateSellerAPI.as_view(), name='update-seller'),
    path('place-order/', PlaceOrderAPI.as_view(), name='place-order'),
]