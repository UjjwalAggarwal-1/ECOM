from django.urls import path

from .views import *

urlpatterns = [
    path("register/", Register.as_view()),
    path("login/", Login.as_view()),
    path("profile/", ProfileDetailAPI.as_view()),
    path("view-cart/", ViewCartAPI.as_view()),
    path("update-cart/", UpdateCartAPI.as_view()),
    path("update-user/", UpdateUserAPI.as_view()),
    path("update-customer/", UpdateCustomerAPI.as_view()),
    path("update-seller/", UpdateSellerAPI.as_view()),
    path("place-order/", PlaceOrderAPI.as_view()),
    path("past-orders/", PastOrdersListAPI.as_view()),
    path("past-order-detail/", PastOrderDetailAPI.as_view()),
    path("create-review/", CreateReviewAPI.as_view()),
]
