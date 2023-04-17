from django.contrib.auth import get_user_model
from django.db import connection
from rest_framework.response import Response
from rest_framework.views import APIView

from core.exceptions import CustomValidationError
from core.helpers import check_keys, get_user_from_request
from core.permissions import IsAuthenticatedByID

User = get_user_model()


"""
Register API View

HTTP Method: POST

URL: /register/

Request Body Parameters:

email: a string representing the user's email address (required)
password: a string representing the user's password (required)
confirm_password: a string representing the user's confirmation password (required)
first_name: a string representing the user's first name (optional)
last_name: a string representing the user's last name (optional)
mobile: a string representing the user's mobile number (required)
age: an integer representing the user's age (optional, default is 1)
sex: a string representing the user's gender (optional)
Response Body:

message: a string indicating the success or failure of the registration process
user_id: an integer representing the ID of the newly registered user (if successful)
Raises:

CustomValidationError: if the request parameters are invalid, the passwords do not match, the email or mobile number is already registered, or the registration process fails.
Login API View

HTTP Method: POST

URL: /login/

Request Body Parameters:

email: a string representing the user's email address (required)
password: a string representing the user's password (required)
Response Body:

message: a string indicating the success or failure of the login process
user_id: an integer representing the ID of the logged-in user (if successful)
Raises:

CustomValidationError: if the email and password combination is invalid.
Profile Detail API View

HTTP Method: GET
URL: /profile/
Request Headers:
Authorization: a token representing the user's authentication credentials (required)
Response Body:
data: an object containing the following fields:
user: an object containing the user's information, including ID, email address, first name, last name, mobile number, age, and gender.
customer: an object containing the customer's information, including total purchases, address line 1, address line 2, city, country, and pincode (if the user is a customer)
seller: an object containing the seller's information, including total sales, store name, address line 1, address line 2, city, country, and pincode (if the user is a seller)
Raises:
CustomValidationError: if the user is not authenticated, or if the user ID cannot be found.
"""


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
            cursor.execute("SELECT * FROM user WHERE email =%s", [email])
            user = cursor.fetchone()
            if user:
                raise CustomValidationError("Email Already Registered!")

            cursor.execute("SELECT * FROM user WHERE mobile =%s", [mobile])
            user = cursor.fetchone()
            if user:
                raise CustomValidationError(
                    "Mobile Number Already Registered!")

            with connection.cursor() as cursor:
                cursor.execute(
                """
                set autocommit=0;
                start transaction;
                insert into user (first_name, last_name, age, sex, email, password, mobile, date_joined)
                values (%s, %s, %s, %s, %s, (select sha1(%s)), %s, now());
                set @user_id = last_insert_id();
                insert into customer (user_id, total_purchases) values (@user_id, 0);
                insert into seller (user_id, total_sales) values (@user_id, 0);
                commit;
                set autocommit=1;
                """,
                    [first_name, last_name, age, sex, email, password, mobile],
                )
            with connection.cursor() as cursor:
                cursor.execute("SELECT id FROM user WHERE email =%s", [email])
                user = cursor.fetchone()
                if not user:
                    raise CustomValidationError("Registration Failed!")
                else:
                    return Response(
                        {
                            "detail": "Registration Successful!",
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
            cursor.execute(
                "\
            select id from user where email = %s and password = (select sha1(%s));\
            ",
                [email, password],
            )
            user = cursor.fetchone()
            if user:
                return Response(
                    {
                        "detail": "Login Successful",
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
                [user.get("id")],
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
                    "pincode": customer[5],
                }

            cursor.execute(
                "SELECT total_sales, store_name, address_line1, address_line2, city, country, pincode FROM seller\
                join address on seller.address_id = address.id \
                join address_pincode on address.id = address_pincode.id \
                WHERE user_id = %s",
                [user.get("id")],
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
                    "pincode": seller[6],
                }

        return Response(
            {"user": user, "seller": seller_data, "customer": customer_data}
        )


"""
ViewCartAPI
This API view returns a list of items in the user's cart. The user must be authenticated and the permission IsAuthenticatedByID must be granted.

HTTP Method: GET

URL: /view_cart/

Request Headers:

Authorization: JWT Token
Response Body:

{
    "data": {
        "cart_items": [
            {
                "item_id": <item_id>,
                "quantity": <quantity>,
                "price": <price>
            },
            ...
        ]
    }
}

UpdateCartAPI
Description
An API endpoint for updating the items in a user's shopping cart. Users must be authenticated and provide an item_id and quantity in the request data.

Endpoint
/api/update_cart

Methods
POST: Update the quantity of an item in the user's shopping cart. If the item is not already in the user's cart, it will be added. If the quantity is set to 0, the item will be removed from the cart.
Request data
json
Copy code
{
    "item_id": 1,
    "quantity": 2
}
Field Name	Type	Description
item_id	number	ID of the item to update in the user's cart
quantity	number	New quantity of the item in the user's cart
Response data
json
Copy code
{
    "message": "Cart updated"
}
Field Name	Type	Description
message	string	Message indicating whether the cart was updated, added, or removed
Error responses
Status code	Response
400	{"error": "Bad Request", "message": "Missing required fields."}<br>{"error": "Bad Request", "message": "Invalid request data."}
401	{"error": "Unauthorized", "message": "Authentication credentials were not provided."}<br>{"error": "Unauthorized", "message": "Authentication failed."}
404	{"error": "Not Found", "message": "Item not found."}
500	{"error": "Internal Server Error", "message": "An error occurred while processing your request."}
"""


class ViewCartAPI(APIView):
    permission_classes = (IsAuthenticatedByID,)

    def get(self, request):
        user = get_user_from_request(request)
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT item.id, item.id, cart.quantity, item.price FROM cart\
                join item on cart.item_id = item.id\
                WHERE customer_id = %s",
                [user.get("id")],
            )
            cart_items = cursor.fetchall()
            cart_items = [
                {"item_id": item[1], "quantity": item[2], "price": item[3]}
                for item in cart_items
            ]

        return Response(cart_items)


class UpdateCartAPI(APIView):
    permission_classes = (IsAuthenticatedByID,)

    def post(self, request):
        data = request.data
        check_keys(data, ["item_id", "quantity"])

        item_id = self.request.data.get("item_id")
        user_id = get_user_from_request(self.request).get("id")

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM cart\
                WHERE customer_id = %s AND item_id = %s",
                [user_id, item_id],
            )
            cart_item = cursor.fetchall()

        if not cart_item:
            cart_item = None
        else:
            cart_item = cart_item[0]

        if not cart_item:
            if int(data["quantity"]) == 0:
                raise CustomValidationError("Item not in cart")
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO cart (customer_id, item_id, quantity) VALUES (%s, %s, %s)",
                    [user_id, int(data["item_id"]), int(data["quantity"])],
                )
            return Response(
                {
                    "detail": "Item added to cart",
                }
            )
        if int(data["quantity"]) == 0:
            with connection.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM cart WHERE customer_id = %s AND item_id = %s",
                    [user_id, data["item_id"]],
                )
            return Response(
                {
                    "detail": "Item removed from cart",
                }
            )

        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE cart SET quantity = %s WHERE customer_id = %s AND item_id = %s",
                [int(data["quantity"]), user_id, int(data["item_id"])],
            )
        return Response(
            {
                "detail": "Cart updated",
            }
        )


"""
UpdateUserAPI

This class is an API view that updates a user's personal information such as their first name, last name, age, and sex. It requires the user to be authenticated and the request should include the fields to be updated. The class makes use of the IsAuthenticatedByID permission class to ensure that the user is authenticated and the get_user_from_request function to get the user object from the request. The check_keys function is used to check if the required fields are present in the request data. The class then executes a SQL query to update the user's information in the database.

UpdateCustomerAPI

This class is an API view that updates a customer's address information such as their address line 1, address line 2, city, country, and pincode. It requires the user to be authenticated and the request should include the fields to be updated. The class makes use of the IsAuthenticatedByID permission class to ensure that the user is authenticated and the get_user_from_request function to get the user object from the request. The check_keys function is used to check if the required fields are present in the request data. The class then executes a series of SQL queries to update the customer's address information in the database. If the address is not already present in the database, a new address is inserted into the address table. If the pincode is not already present in the database, a new row is inserted into the address_pincode table. Finally, the customer's address_id is updated in the customer table.

UpdateSellerAPI

This class is an API view that updates a seller's store information such as their store name, address line 1, address line 2, city, country, and pincode. It requires the user to be authenticated and the request should include the fields to be updated. The class makes use of the IsAuthenticatedByID permission class to ensure that the user is authenticated and the get_user_from_request function to get the user object from the request. The check_keys function is used to check if the required fields are present in the request data. The class then executes a series of SQL queries to update the seller's store information in the database. If the address is not already present in the database, a new address is inserted into the address table. If the pincode is not already present in the database, a new row is inserted into the address_pincode table. Finally, the seller's store_name and address_id are updated in the seller table.
"""


class UpdateUserAPI(APIView):
    permission_classes = (IsAuthenticatedByID,)

    def put(self, request):
        user = get_user_from_request(request)
        data = request.data
        check_keys(data, ["first_name", "last_name", "age", "sex"])
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
                    user.get("id"),
                ],
            )
        return Response({"detail": "User updated"})


class UpdateCustomerAPI(APIView):
    permission_classes = (IsAuthenticatedByID,)

    def put(self, request):
        user = get_user_from_request(request)
        data = request.data
        check_keys(
            data, ["address_line1", "city", "country", "pincode"]
        )
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id FROM address WHERE address_line1 = %s AND address_line2 = %s AND city = %s AND country = %s",
                [
                    data["address_line1"],
                    data.get("address_line2", ""),
                    data["city"],
                    data["country"],
                ],
            )
            address = cursor.fetchone()
            if not address:
                cursor.execute(
                    "INSERT INTO address (address_line1, address_line2, city, country) VALUES (%s, %s, %s, %s);",
                    [
                        data["address_line1"],
                        data.get("address_line2", ""),
                        data["city"],
                        data["country"],
                    ],
                )
                cursor.execute("select max(id) from address;")
                address = cursor.fetchone()
            address_id = address[0]
            cursor.execute(
                "SELECT id FROM address_pincode WHERE id = %s AND pincode = %s",
                [address_id, data["pincode"]],
            )
            address_pincode = cursor.fetchone()
            if not address_pincode:
                cursor.execute(
                    "INSERT INTO address_pincode (id, pincode) VALUES (%s, %s)",
                    [address_id, data["pincode"]],
                )
            cursor.execute(
                "SELECT user_id FROM customer WHERE user_id = %s", [user.get("id")]
            )
            cursor.execute(
                "UPDATE customer SET address_id = %s WHERE user_id = %s",
                [address_id, user.get("id")],
            )
        return Response({"detail": "Customer updated"})


class UpdateSellerAPI(APIView):
    permission_classes = (IsAuthenticatedByID,)

    def put(self, request):
        user = get_user_from_request(request)
        data = request.data
        check_keys(
            data,
            [
                "store_name",
                "address_line1",
                "city",
                "country",
                "pincode",
            ],
        )
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id FROM address WHERE address_line1 = %s AND address_line2 = %s AND city = %s AND country = %s",
                [
                    data["address_line1"],
                    data.get("address_line2", ""),
                    data["city"],
                    data["country"],
                ],
            )
            address = cursor.fetchone()
            if not address:
                cursor.execute(
                    "INSERT INTO address (address_line1, address_line2, city, country) VALUES (%s, %s, %s, %s);",
                    [
                        data["address_line1"],
                        data.get("address_line2", ""),
                        data["city"],
                        data["country"],
                    ],
                )
                cursor.execute("select max(id) from address;")
                address = cursor.fetchone()
            address_id = address[0]
            cursor.execute(
                "SELECT id FROM address_pincode WHERE id = %s AND pincode = %s",
                [address_id, data["pincode"]],
            )
            address_pincode = cursor.fetchone()
            if not address_pincode:
                cursor.execute(
                    "INSERT INTO address_pincode (id, pincode) VALUES (%s, %s)",
                    [address_id, data["pincode"]],
                )

            cursor.execute(
                "UPDATE seller SET store_name = %s, address_id = %s WHERE user_id = %s",
                [data["store_name"], address_id, user.get("id")],
            )

        return Response({"detail": "Seller updated"})


"""
PlaceOrderAPI: This class handles placing an order. It accepts a POST request and expects the following parameters in the request body:
payment_method: The payment method used for the order.
If the user is authenticated, it gets the user_id from the request and uses it to check if the user is a customer. If the user is not a customer, it returns a 401 Unauthorized response with the message "You are not a customer". If the user is a customer, it fetches the items in the customer's cart and calculates the total amount for the items. It then generates a unique order ID and inserts a new order record in the database. For each item in the cart, it inserts a new order item record and deletes the item from the cart. It returns a 200 OK response with the message "Order placed" on successful execution.

PastOrdersListAPI: This class handles retrieving a list of past orders for the authenticated user. It accepts a GET request and expects no parameters. If the user is authenticated, it gets the user_id from the request and uses it to check if the user is a customer. If the user is not a customer, it returns a 401 Unauthorized response with the message "You are not a customer". If the user is a customer, it retrieves all the orders for the customer from the database and returns a 200 OK response with the order details.

PastOrderDetailAPI: This class handles retrieving the details of a specific past order for the authenticated user. It accepts a GET request and expects the following query parameter:

order_id: The ID of the order to retrieve.
If the user is authenticated, it gets the user_id from the request and uses it to check if the user is a customer. If the user is not a customer, it returns a 401 Unauthorized response with the message "You are not a customer". If the user is a customer and the order_id is provided, it retrieves the order details from the database and returns a 200 OK response with the order details and order items. If the order_id is not provided, it returns a 400 Bad Request response with the message "Order id is required".
"""


class PlaceOrderAPI(APIView):
    permission_classes = (IsAuthenticatedByID,)

    def post(self, request):
        user = get_user_from_request(request)
        data = request.data
        # check_keys(data, ["payment_method"])
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT user_id, address_id FROM customer WHERE user_id = %s", [
                    user.get("id")]
            )
            customer = cursor.fetchone()
            if not customer:
                raise CustomValidationError("You are not a customer")
            customer_id = customer[0]
            address_id = customer[1]
            if not address_id:
                raise CustomValidationError("Address is required")
            cursor.execute(
                "SELECT customer_id, customer_id, item_id, quantity FROM cart WHERE customer_id = %s",
                [customer_id],
            )
            cart_items = cursor.fetchall()
            if not cart_items:
                raise CustomValidationError("Cart is empty")
            cursor.execute(
                "select sum(price*quantity) as total from cart join item on cart.item_id = item.id where customer_id = %s",
                [customer_id],
            )
            total = cursor.fetchone()[0]
            cursor.execute(
                "set @gen_uid = concat(%s, sha1(now()));\
                set @address_id = (select address_id from customer where user_id = %s);\
                INSERT INTO `order` (customer_id, amount, payment_uid, address_id) VALUES (%s, %s, @gen_uid, @address_id);\
                ;",
                [customer_id, customer_id, customer_id, total],
            )
            cursor.execute("SELECT max(id) FROM `order`")
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
                    "UPDATE item SET stock = stock - %s WHERE id = %s;"
                    "commit;",
                    [cart_item[2]]
                    + [user.get("id")]
                    + [user.get("id")]
                    + [order_id, cart_item[2], cart_item[3]]
                    + [customer_id, cart_item[2]]
                    + [cart_item[3], cart_item[2]],
                )
        return Response({"detail": "Order placed"})


class PastOrdersListAPI(APIView):
    permission_classes = (IsAuthenticatedByID,)

    def get(self, request):
        user = get_user_from_request(request)
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT user_id FROM customer WHERE user_id = %s", [
                    user.get("id")]
            )
            customer = cursor.fetchone()
            if not customer:
                raise CustomValidationError("You are not a customer")
            customer_id = customer[0]
            cursor.execute(
                "SELECT id, payment_uid, amount, order_time FROM `order` WHERE customer_id = %s",
                [customer_id],
            )
            orders = cursor.fetchall()
            orders = [
                {
                    "id": order[0],
                    "payment_uid": order[1],
                    "amount": order[2],
                    "created_at": order[3].strftime("%d-%m-%Y %H:%M"),
                }
                for order in orders
            ]

            return Response(orders)


class PastOrderDetailAPI(APIView):
    permission_classes = (IsAuthenticatedByID,)

    def get(self, request):
        order_id = request.query_params.get("order_id")
        user = get_user_from_request(request)
        if not order_id:
            raise CustomValidationError("Order id is required")
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT user_id FROM customer WHERE user_id = %s", [
                    user.get("id")]
            )
            customer = cursor.fetchone()
            if not customer:
                raise CustomValidationError("You are not a customer")
            customer_id = customer[0]
            cursor.execute(
                "SELECT `order`.id, payment_uid, amount, order_time, address_line1, adderss_line2, city, country, pincode FROM `order` " 
                "left JOIN address on address.id = `order`.address_id "
                "left JOIN address_pincode on address_pincode.id = address.id "
                "WHERE customer_id = %s AND `order`.id = %s ; ",
                [customer_id, order_id],
            )
            order = cursor.fetchone()
            if not order:
                raise CustomValidationError("Order not found")
            order = {
                "id": order[0],
                "payment_uid": order[1],
                "amount": order[2],
                "order_time": order[3].strftime("%d-%m-%Y %H:%M"),
                "address_line1": order[4],
                "address_line2": order[5],
                "city": order[6],
                "country": order[7],
                "pincode": order[8],
            }
            cursor.execute(
                "SELECT item_id, quantity, price, status FROM orderitem WHERE order_id = %s",
                [order_id],
            )
            order_items = cursor.fetchall()
            order_items = [
                {
                    "item_id": order_item[0],
                    "quantity": order_item[1],
                    "price": order_item[2],
                    "status": order_item[3],
                }
                for order_item in order_items
            ]
            return Response({"order": order, "order_items": order_items})
