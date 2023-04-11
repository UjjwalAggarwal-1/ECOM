from rest_framework import serializers
from market.models import *
from users.serializers import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'image')


class ItemListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = "__all__"


class ItemDetailSerializer(serializers.ModelSerializer):
    seller = CustomerSerializer(read_only=True)
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Item
        fields = "__all__"
        