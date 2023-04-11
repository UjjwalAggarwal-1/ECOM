from .models import *
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from django.contrib.auth import get_user_model
from django.db.models import Sum

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
        data["cart_count"] = instance.customer.cart_set.aggregate(Sum('quantity')).get('quantity__sum', 0)

        c_data = FullCustomerSerializer(instance.customer).data
        s_data = FullSellerSerializer(instance.seller).data

        return {**data, **c_data, **s_data}