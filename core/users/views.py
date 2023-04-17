from rest_framework.views import APIView
from rest_framework.response import Response
from core.exceptions import CustomValidationError

from core.permissions import IsAuthenticatedByID
from core.helpers import check_keys, get_user_from_request
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
            age = request.data.get("age", 1)
            sex = request.data.get("sex", "")
        except KeyError:
            raise CustomValidationError("Invalid request Parameters")

        if password != confirm_password:
            raise CustomValidationError("Passwords do not match!")

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM user WHERE email =%s", 
                [email]
            )
            user = cursor.fetchone()
            if user:
                raise CustomValidationError("Email Already Registered!")

            cursor.execute(
                "SELECT * FROM user WHERE mobile =%s", 
                [mobile]
            )
            user = cursor.fetchone()
            if user:
                raise CustomValidationError("Mobile Number Already Registered!")
        
            with connection.cursor() as cursor:
                cursor.execute(
                """
                start transaction;
                insert into user (first_name, last_name, age, sex, email, password, mobile, date_joined)
                values (%s, %s, %s, %s, %s, (select sha1(%s)), %s, now());
                set @user_id = last_insert_id();
                insert into customer (user_id, total_purchases) values (@user_id, 0);
                insert into seller (user_id, total_sales) values (@user_id, 0);
                commit;
                """,
                [first_name, last_name, age, sex, email, password, mobile]
                )
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id FROM user WHERE email =%s", 
                    [email]
                )
                user = cursor.fetchone()
                if not user:
                    raise CustomValidationError("Registration Failed!")
                else:
                    return Response(
                        {
                            "message": "Registration Successful!",
                            "user_id": user[0],
                        }
                    )


class Login(APIView):
    def post(self, request):
        data = request.data
        
        check_keys(data, ["email", "password"])
        email = data.get("email", None)
        password = data.get("password", None)

        with connection.cursor() as cursor:
            cursor.execute("\
            select id from user where email = %s and password = (select sha1(%s));\
            ",
            [email, password],
            )
            user = cursor.fetchone()
            if user:
                return Response(
                    {
                        "message": "Login Successful",
                        "user_id": user[0],
                    }
                )
            else:
                raise CustomValidationError("Invalid Credentials")


class ProfileDetailAPI(APIView):
    permission_classes = (IsAuthenticatedByID,)

    def get(self, request):
        user = get_user_from_request(request)
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT total_purchases, address_line1, address_line2, city, country, pincode FROM customer\
                join address on customer.address_id = address.id \
                join address_pincode on address.id = address_pincode.id \
                WHERE user_id = %s", 
                [user.get('id')]
            )
            customer = cursor.fetchone()
            customer_data = {}
            if customer:
                customer_data = {
                    "total_purchases": customer[0],
                    "address_line1": customer[1],
                    "address_line2": customer[2],
                    "city": customer[3],
                    "country": customer[4],
                    "pincode": customer[5]
                }

            cursor.execute(
                "SELECT total_sales, store_name, address_line1, address_line2, city, country, pincode FROM seller\
                join address on seller.address_id = address.id \
                join address_pincode on address.id = address_pincode.id \
                WHERE user_id = %s", 
                [user.get('id')]
            )
            seller = cursor.fetchone()
            seller_data = {}
            if seller:
                seller_data = {
                    "total_sales": seller[0],
                    "store_name": seller[1],
                    "address_line1": seller[2],
                    "address_line2": seller[3],
                    "city": seller[4],
                    "country": seller[5],
                    "pincode": seller[6]
                }

        return Response(
            {
                "data": {
                    "user": user,
                    'seller': seller_data,
                    'customer': customer_data
                }
            }
        )


class ViewCartAPI(APIView):
    permission_classes = (IsAuthenticatedByID,)

    def get(self, request):
        user = get_user_from_request(request)
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT item.id, item.id, cart.quantity, item.price FROM cart\
                join item on cart.item_id = item.id\
                WHERE customer_id = %s", 
                [user.get('id')]
            )
            cart_items = cursor.fetchall()
            cart_items = [
                {
                    "item_id": item[1],
                    "quantity": item[2],
                    "price": item[3]
                } for item in cart_items
            ]

        return Response(
            {
                "data": {
                    "cart_items": cart_items
                }
            }
        )    


class UpdateCartAPI(APIView):

    permission_classes = (IsAuthenticatedByID,)

    def post(self, request):
        data = request.data
        check_keys(data, ["item_id", "quantity"])

        item_id = self.request.data.get("item_id")
        user_id = get_user_from_request(self.request).get('id')
        
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM cart\
                WHERE customer_id = %s AND item_id = %s", 
                [user_id, item_id]
            )
            cart_item = cursor.fetchall()

        if not cart_item:
            cart_item = None
        else:
            cart_item = cart_item[0]

        if not cart_item:
            if int(data['quantity']) == 0:
                return Response(
                    {
                        "message": "Item fell out of cart",
                    }
                )
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO cart (customer_id, item_id, quantity) VALUES (%s, %s, %s)", 
                    [user_id, int(data["item_id"]), int(data["quantity"])],
                )
            return Response(
                {
                    "message": "Item added to cart",
                }
            )
        if int(data["quantity"]) == 0:
            with connection.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM cart WHERE customer_id = %s AND item_id = %s", 
                    [user_id, data["item_id"]]
                )
            return Response(
                {
                    "message": "Item removed from cart",
                }
            )
        
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE cart SET quantity = %s WHERE customer_id = %s AND item_id = %s", 
                [int(data['quantity']), user_id, int(data["item_id"])]
            )
        return Response(
            {
                "message": "Cart updated",
            }
        )
    

class UpdateUserAPI(APIView):
    permission_classes = (IsAuthenticatedByID,)

    def put(self, request):
        user = get_user_from_request(request)
        data = request.data
        check_keys(data, ["first_name", "last_name", 'age', 'sex'])
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE user \
                set first_name = %s,\
                last_name = %s,\
                age = %s,\
                sex = %s \
                where id = %s",
                [
                    data["first_name"],
                    data["last_name"],
                    data["age"],
                    data["sex"],
                    user.get('id')
                ]
            )
        return Response({'detail':"User updated"})


class UpdateCustomerAPI(APIView):
    permission_classes = (IsAuthenticatedByID,)

    def patch(self, request):
        user = get_user_from_request(request)
        data = request.data
        check_keys(data, ["address_line1", "address_line2", "city", "country", "pincode"])
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id FROM address WHERE address_line1 = %s AND address_line2 = %s AND city = %s AND country = %s", 
                [data["address_line1"], data["address_line2"], data["city"], data["country"]]
            )
            address = cursor.fetchone()
            if not address:
                cursor.execute(
                    "INSERT INTO address (address_line1, address_line2, city, country) VALUES (%s, %s, %s, %s) RETURNING id", 
                    [data["address_line1"], data["address_line2"], data["city"], data["country"]]
                )
                address = cursor.fetchone()
            address_id = address[0]
            cursor.execute(
                "SELECT id FROM address_pincode WHERE id = %s AND pincode = %s", 
                [address_id, data["pincode"]]
            )
            address_pincode = cursor.fetchone()
            if not address_pincode:
                cursor.execute(
                    "INSERT INTO address_pincode (id, pincode) VALUES (%s, %s)", 
                    [address_id, data["pincode"]]
                )
            cursor.execute(
                "SELECT id FROM customer WHERE user_id = %s", 
                [user.get('id')]
            )
            cursor.execute(
                "UPDATE customer SET address_id = %s WHERE user_id = %s", 
                [address_id, user.get('id')]
            )
        return Response({'detail':"Customer updated"})


class UpdateSellerAPI(APIView):
    permission_classes = (IsAuthenticatedByID,)

    def patch(self, request):
        user = get_user_from_request(request)
        data = request.data
        check_keys(data, ["store_name", "address_line1", "address_line2", "city", "country", "pincode"])
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id FROM address WHERE address_line1 = %s AND address_line2 = %s AND city = %s AND country = %s", 
                [data["address_line1"], data["address_line2"], data["city"], data["country"]]
            )
            address = cursor.fetchone()
            if not address:
                cursor.execute(
                    "INSERT INTO address (address_line1, address_line2, city, country) VALUES (%s, %s, %s, %s) RETURNING id", 
                    [data["address_line1"], data["address_line2"], data["city"], data["country"]]
                )
                address = cursor.fetchone()
            address_id = address[0]
            cursor.execute(
                "SELECT id FROM address_pincode WHERE id = %s AND pincode = %s", 
                [address_id, data["pincode"]]
            )
            address_pincode = cursor.fetchone()
            if not address_pincode:
                cursor.execute(
                    "INSERT INTO address_pincode (id, pincode) VALUES (%s, %s)", 
                    [address_id, data["pincode"]]
                )
            
            cursor.execute(
                "UPDATE seller SET store_name = %s, address_id = %s WHERE user_id = %s", 
                [data["store_name"], address_id, user.get('id')]
            )

        return Response({'detail':"Seller updated"})
    

class PlaceOrderAPI(APIView):
    permission_classes = (IsAuthenticatedByID,)

    def post(self, request):
        user = get_user_from_request(request)
        data = request.data
        # check_keys(data, ["payment_method"])
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT user_id FROM customer WHERE user_id = %s", 
                [user.get('id')]
            )
            customer = cursor.fetchone()
            if not customer:
                return Response(
                    {
                        "message": "You are not a customer",
                    }
                )
            customer_id = customer[0]
            cursor.execute(
                "SELECT customer_id, customer_id, item_id, quantity FROM cart WHERE customer_id = %s", 
                [customer_id]
            )
            cart_items = cursor.fetchall()
            if not cart_items:
                return Response(
                    {
                        "message": "Your cart is empty",
                    }
                )
            cursor.execute(
                'select sum(price*quantity) as total from cart join item on cart.item_id = item.id where customer_id = %s',
                [customer_id]
            )
            total = cursor.fetchone()[0]
            cursor.execute(
                "set @gen_uid = concat(%s, sha1(now()));\
                INSERT INTO `order` (customer_id, amount, uid) VALUES (%s, %s, @gen_uid );\
                ;", 
                [customer_id, customer_id, total]
            )
            cursor.execute(
                "SELECT max(id) FROM `order`"
            )
            order_id = cursor.fetchone()[0]

            for cart_item in cart_items:
                cursor.execute(
                    "start transaction;"
                    "set @price = (select price from item where id = %s);"
                    "set @from_address_id = (select address_id from seller where user_id = %s);"
                    "set @to_address_id = (select address_id from customer where user_id = %s);"
                    "INSERT INTO orderitem (order_id, item_id, quantity, price, from_address_id, to_address_id, status) VALUES\
                    (%s, %s, %s, @price, @from_address_id, @to_address_id, 'ORDER_PLACED');"
                    "DELETE FROM cart WHERE customer_id = %s AND item_id = %s;"
                    "commit;", 
                    [cart_item[2]]+
                    [user.get('id')]+
                    [user.get('id')]+
                    [order_id, cart_item[2], cart_item[3]]+
                    [customer_id, cart_item[2]]
                    )
        return Response({'detail':"Order placed"})