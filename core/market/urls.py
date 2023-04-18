from django.urls import include, path
from market.views import *

urlpatterns = [
    path("item-list/", ItemListAPI.as_view()),
    path("category-list/", CategoryListAPI.as_view()),
    path("item/", ItemRetreiveAPI.as_view()),
    path("verify-coupon/", VerifyCouponAPI.as_view()),
    path("create-item/", CreateItemAPI.as_view()),
    path("update-item/", UpdateItemAPI.as_view()),
    path("get-seller-items/", GetSellerItemsAPI.as_view()),
]
