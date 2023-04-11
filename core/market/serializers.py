from rest_framework import serializers
from market.models import *
from users.models import *
from users.serializers import *
from django.db import connection
from django.db.models import Avg

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'image')


class ItemListSerializer(serializers.ModelSerializer):
    seller_name = serializers.CharField(source='seller.user.first_name', read_only=True)
    image = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = ("id", "name", "price", "image", "seller_name", 'rating')
    
    def get_image(self, obj):
        return obj.images.first().image.url if obj.images.first() else None
    
    def get_rating(self, obj):
        return Review.objects.filter(item=obj).aggregate(Avg('rating'))['rating__avg'] or 0



class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('item','quantity')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        item_data = ItemListSerializer(instance.item).data
        data.pop('item')
        return {**item_data,**data}
    

class ItemSerializer(serializers.ModelSerializer):
    seller_name = serializers.CharField(source='seller.user.first_name', read_only=True)
    rating = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = ("id", "name", "price", "seller_name", 'rating', 'description', 'total_sale', 'images')

    def get_rating(self, obj):
        return Review.objects.filter(item=obj).aggregate(Avg('rating'))['rating__avg'] or 0

    def get_images(self, obj):
        return [image.image.url for image in obj.images.all() if image.image]
