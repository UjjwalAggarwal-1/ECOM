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


class ItemListAPI(generics.ListAPIView):
    serializer_class = ItemListSerializer
    permission_classes = []

    def get_queryset(self):
        queryset = Item.objects.raw(
            'SELECT * FROM market_item'
            )
        category = self.request.query_params.get('category', None)
        search = self.request.query_params.get('search', None)
        trending = self.request.query_params.get('trending', None)
        # if category and search:
        #     return None
        if category is not None:
            queryset = Item.objects.raw(
                'SELECT *  FROM `market_item` \
                INNER JOIN `market_category` ON (`market_item`.`categories_id` = `market_category`.`id`)\
                WHERE `market_category`.`name` = %s', 
                [category]
                )
        if search is not None:
            queryset = Item.objects.raw(
                'SELECT * FROM market_item WHERE name LIKE %s \
                UNION SELECT * FROM market_item \
                INNER JOIN `market_category` ON (`market_item`.`categories_id` = `market_category`.`id`)\
                WHERE `market_category`.`name` LIKE %s', 
                ['%'+search+'%', '%'+search+'%'] 
                )
            
        if trending is not None:
            queryset = Item.objects.raw(
                'SELECT * FROM market_item ORDER BY total_sale DESC LIMIT %s',
                [int(trending)]
                )
        return queryset


class CategoryListAPI(generics.ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = []
    queryset = Category.objects.raw(
        'SELECT * FROM market_category'
        )


class ItemRetreiveAPI(generics.APIView):
    serializer_class = ItemSerializer
    permission_classes = []
    queryset = Item.objects.all()

    def get_object(self):
        pk = self.request.query_params.get('id', None)
        try:
            return Item.objects.get(pk=pk)
        except Item.DoesNotExist:
            raise CustomValidationError("Item does not exist")