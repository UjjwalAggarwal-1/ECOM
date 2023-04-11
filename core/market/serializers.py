from rest_framework import serializers
from market.models import *
from users.models import *
from users.serializers import *

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
        return 4.5
    


class ItemDetailSerializer(serializers.ModelSerializer):
    seller = CustomerSerializer(read_only=True)
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Item
        fields = "__all__"
        

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('item','quantity')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        item_data = ItemListSerializer(instance.item).data
        data.pop('item')
        return {**item_data,**data}
    
