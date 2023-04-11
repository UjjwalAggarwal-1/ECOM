from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from core.exceptions import CustomValidationError
from .models import *
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

        if User.objects.filter(email=email).exists():
            raise CustomValidationError("Email Already Registered!")
        if User.objects.filter(mobile=mobile).exists():
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
                Customer.objects.create(user=user)
                Seller.objects.create(user=user)
                
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
            **UserSerializer(user).data,
            "access": str(refresh.access_token),
            # "refresh": str(refresh),
            # **settings.SIMPLE_JWT,
        }

    return response


class Login(APIView):
    def post(self, request):
        data = request.data
        # check_keys(data, ["user_type"])

        # if not data["user_type"] in ["C", "S"]:
        #     raise CustomValidationError("Invalid Data: user_type")

        check_keys(data, ["email", "password"])
        email = data.get("email", None)
        password = data.get("password", None)
        auth_user = authenticate(username=email, password=password)
        if not auth_user:
            raise CustomValidationError("Invalid credentials")
        # try:
        #     if data["user_type"] == "C":
        #         if not auth_user.customer:
        #             raise CustomValidationError("Invalid credentials")
        #     else:
        #         if not auth_user.seller:
        #             raise CustomValidationError("Invalid credentials")
        # except:
        #     raise CustomValidationError("Need to sign up first")

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
    serializer_class = ProfileDetailsSerializer

    def get_object(self):
        return self.request.user
