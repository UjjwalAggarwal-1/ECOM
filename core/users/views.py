from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from core.exceptions import CustomValidationError
from .models import *
from market.serializers import *
from django.db import transaction
from django.contrib.auth import authenticate, login
from django.conf import settings
from core.helpers import check_keys
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.contrib.auth import logout
from rest_framework_simplejwt.views import TokenRefreshView
from django.db import connection

from django.contrib.auth import get_user_model

User = get_user_model()


class Register(APIView):

    def post(self, request):
        try:
            email = request.data["email"].lower()
            password = request.data["password"]
            confirm_password = request.data["confirm_password"]
            first_name = request.data.get("first_name", "")
            last_name = request.data.get("last_name", "")
            mobile = request.data["mobile"]
            age = request.data.get("age", 0)
            sex = request.data.get("sex", "")
        except KeyError:
            raise CustomValidationError("Invalid request Parameters")

        if password != confirm_password:
            raise CustomValidationError("Passwords do not match!")

        with connection.cursor() as cursor:
            # if User.objects.filter(email=email).exists():
            #     raise CustomValidationError("Email Already Registered!")
            cursor.execute(
                "SELECT * FROM users_user WHERE email =%s", 
                [email]
            )
            user = cursor.fetchone()
            if user:
                raise CustomValidationError("Email Already Registered!")
            
            # if User.objects.filter(mobile=mobile).exists():
            #     raise CustomValidationError("Mobile Number Already Registered!")
            cursor.execute(
                "SELECT * FROM users_user WHERE mobile =%s", 
                [mobile]
            )
            user = cursor.fetchone()
            if user:
                raise CustomValidationError("Mobile Number Already Registered!")
        
        with transaction.atomic():
            try:
                user = User.objects.create_user(
                    username = email,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    mobile=mobile,
                    age=age,
                    sex = sex
                )
                user.set_password(password)
                user.save()
                user_id = user.id

                with connection.cursor() as cursor:
                    # Customer.objects.create(user=user)
                    cursor.execute(
                        "INSERT INTO users_customer (user_id, total_purchases) VALUES (%s, 0)",
                          [user_id] 
                    )
                    # Seller.objects.create(user=user)
                    cursor.execute(
                        "INSERT INTO users_seller (user_id, total_sales) VALUES (%s, 0)",
                          [user_id] 
                    )

            except Exception as e:
                print("errror", str(e))
                raise CustomValidationError("Unable to register. Try again later.")
        return Response(
            {
                "message": "Registration Successful!",
                "user": UserSerializer(user).data,
            }
        )
    
def login_response(user):
    if not user:
        raise CustomValidationError("Invalid Credentials")
    refresh = RefreshToken.for_user(user)
    response = Response()
    response.data = {
            "message": "Login Successful",
            **UserLoginResponseSerializer(user).data,
            "access": str(refresh.access_token),
            # "refresh": str(refresh),
            # **settings.SIMPLE_JWT,
        }

    return response


class Login(APIView):
    def post(self, request):
        data = request.data
        
        check_keys(data, ["email", "password"])
        email = data.get("email", None)
        password = data.get("password", None)
        auth_user = authenticate(username=email, password=password)
        if not auth_user:
            raise CustomValidationError("Invalid credentials")

        login(request, auth_user)
        auth_user.last_login = timezone.now()
        auth_user.save()

        return login_response(auth_user)


class Logout(APIView):
    def post(self, request):
        logout(request)
        return Response(
            {
                "message": "Logout Successful",
            }
        )


class ProfileDetailAPI(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserLoginResponseSerializer

    def get_object(self):
        user_id = self.request.user.id
        user = User.objects.raw(
                "SELECT * FROM users_user WHERE id = %s", 
                [user_id]
            )
        if not user:
            return None
        user = user[0]
        return user


class ViewCartAPI(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CartSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        cart_items = Cart.objects.raw(
            "SELECT * FROM users_cart WHERE customer_id = %s", 
            [user_id]
        )
        return cart_items
    

class UpdateCartAPI(generics.UpdateAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = CartSerializer

    def get_object(self):
        item_id = self.request.data.get("item_id")
        if not item_id:
            raise CustomValidationError("Invalid request parameters")
        
        user_id = self.request.user.id
        
        cart_item = Cart.objects.raw(
            "SELECT * FROM users_cart WHERE customer_id = %s AND item_id = %s", 
            [user_id, item_id]
        )
        if not cart_item:
            return None
        cart_item = cart_item[0]
        return cart_item
    
    def post(self, request):
        data = request.data
        check_keys(data, ["item_id", "quantity"])
        cart_item = self.get_object()
        if not cart_item:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO users_cart (customer_id, item_id, quantity) VALUES (%s, %s, %s)", 
                    [request.user.id, int(data["item_id"]), int(data["quantity"])],
                )
            return Response(
                {
                    "message": "Item added to cart",
                }
            )
        if int(data["quantity"]) == 0:
            with connection.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM users_cart WHERE customer_id = %s AND item_id = %s", 
                    [request.user.id, data["item_id"]]
                )
            return Response(
                {
                    "message": "Item removed from cart",
                }
            )
        
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE users_cart SET quantity = %s WHERE customer_id = %s AND item_id = %s", 
                [int(data['quantity']), request.user.id, int(data["item_id"])]
            )
        return Response(
            {
                "message": "Cart updated",
            }
        )
    

class UpdateUserAPI(generics.UpdateAPIView):
    model = User
    permission_classes = (IsAuthenticated,)
    serializer_class = FullUserSerializer

    def get_object(self):
        return self.request.user

class UpdateCustomerAPI(generics.UpdateAPIView):
    model = Customer
    permission_classes = (IsAuthenticated,)
    serializer_class = FullCustomerSerializer

    def get_object(self):
        return self.request.user.customer

class UpdateSellerAPI(generics.UpdateAPIView):
    model = Seller
    permission_classes = (IsAuthenticated,)
    serializer_class = FullSellerSerializer

    def get_object(self):
        return self.request.user.seller
