from django.urls import path, include
from market.views import *


urlpatterns = [
    path('item-list/', ItemListAPI.as_view()),
    path('category-list/', CategoryListAPI.as_view()),
    path('item/', ItemRetreiveAPI.as_view()),
]