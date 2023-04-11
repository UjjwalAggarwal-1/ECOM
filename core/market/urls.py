from django.urls import path, include
from market.views import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
# router.register(r'items', ItemViewSet, basename='item')
# router.register(r'moderator-items', ModeratorItemViewSet, basename = "moderator-item")
# router.register(r'reports', ReportViewSet, basename = 'report')
# router.register(r'category', CategoryViewSet, basename = 'category')
# urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)),
    path('item-list/', ItemListAPI.as_view()),
    path('category-list/', CategoryListAPI.as_view()),
    path('item/', ItemRetreiveAPI.as_view()),
    # path('year/list/', YearListAPIView.as_view()),
    # path('condition/list/', ConditionListAPIView.as_view()),
    # path('price_filter/list/', price_filter_list),
    # path('update_favourite/<str:static_id>/', MakeFavouriteAPI.as_view()),
    # path('report/<str:static_id>/', ReportAPI.as_view()),
    # path('lock/<str:room_id>/', LockItem.as_view()),
    # path('sell_item/<str:static_id>/', SellItem.as_view()),
    # path('delete_image/', DeleteItemImageAPI.as_view()),
]