from .models import *
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.db import connection

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            # "id",
            "email",
        )
        # exclude = ('password','user_permissions','groups', 'is_staff', 'is_superuser', 'is_active', 'last_login', 'date_joined', 'is_deleted')
        extra_kwargs = {"password": {"write_only": True}}


class ProfileDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "mobile",
            "age",
            "sex",
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["member_since"] = instance.date_joined.strftime("%B %d, %Y")
        # data["last_login"] = instance.last_login.strftime("%H:%M, %B %d, %Y")

        return data


class TokenRefreshSerializer(TokenRefreshSerializer):
    pass


class FullCustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = "__all__"


class FullSellerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Seller
        fields = "__all__"


class UserLoginResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "mobile",
            "age",
            "sex",
        )
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["member_since"] = instance.date_joined.strftime("%B %d, %Y")

        customer_id = instance.id
        print("customer_id", customer_id)
        with connection.cursor() as cursor:
                ret = Cart.objects.raw(
                    "SELECT 1 as id, customer_id, SUM(quantity) as total_items FROM users_cart\
                          WHERE customer_id = %s GROUP BY customer_id ", 
                    [customer_id]
                )
        data["cart_count"] = int(ret[0].total_items)

        c_data = FullCustomerSerializer(instance.customer).data
        s_data = FullSellerSerializer(instance.seller).data

        return {**data, **c_data, **s_data}