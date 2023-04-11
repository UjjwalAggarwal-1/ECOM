from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from core.exceptions import CustomValidationError
from django.db import transaction
from django.conf import settings
from core.helpers import check_keys
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import *
from .serializers import *
from core.permissions import *


# class CategoryViewSet(viewsets.ModelViewSet):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#     permission_classes = [IsAuthenticated]


# class ItemViewSet(viewsets.ModelViewSet):
#     queryset = Item.objects.all()
#     serializer_class = ItemDetailSerializer
#     permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

#     def get_queryset(self):
#         queryset = Item.objects.all()
#         category = self.request.query_params.get('category', None)
#         if category is not None:
#             queryset = queryset.filter(category__name=category.upper())
#         return queryset
    
#     def perform_create(self, serializer):
#         serializer.save(seller=self.request.user.customer)


class ItemListAPI(generics.ListAPIView):
    serializer_class = ItemListSerializer
    permission_classes = []

    def get_queryset(self):
        queryset = Item.objects.raw('SELECT * FROM market_item')
        category = self.request.query_params.get('category', None)
        if category is not None:
            queryset = Item.objects.raw('SELECT * FROM market_item WHERE category_id = %s', [category])
        return queryset


class CategoryListAPI(generics.ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = []
    queryset = Category.objects.raw('SELECT * FROM market_category')
