from django.db import connection
from django.http.response import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from core.exceptions import CustomValidationError
from core.helpers import check_keys
from core.permissions import IsAuthenticatedByID

"""
The code defines three classes, each subclassing Django REST framework's APIView: ItemListAPI, CategoryListAPI, and ItemRetrieveAPI.

The ItemListAPI is responsible for fetching a list of items from the database based on optional query parameters passed with the request (category, search, and trending). The fetched data is then transformed into a JSON format and returned as a HTTP response.

The CategoryListAPI class retrieves a list of categories from the database and returns it as a JSON formatted response.

The ItemRetrieveAPI retrieves detailed information about a single item identified by the id parameter. If no id parameter is provided, a CustomValidationError is raised. The fetched data is transformed and returned as a JSON response. Additionally, the method also retrieves any reviews associated with the item by joining with the order and user tables.
"""


class ItemListAPI(APIView):
    permission_classes = []

    def get_data(self):
        with connection.cursor() as cursor:
            cursor.execute(
                'SELECT item.id, item.name, item.price, concat(user.first_name, " ", user.last_name) as seller_name, \
            ifnull(avg(rating),0) as rating,item.mrp, (item.mrp-item.price)*100/item.mrp as discount FROM item \
            join user on item.seller_id = user.id\
            left join review on item.id = review.item_id\
            group by item.id\
            ;'
            )
            queryset = cursor.fetchall()

        category = self.request.query_params.get("category", None)
        search = self.request.query_params.get("search", None)
        trending = self.request.query_params.get("trending", None)

        if category is not None:
            with connection.cursor() as cursor:
                cursor.execute(
                    'SELECT item.id, item.name, price, concat(user.first_name, " ", user.last_name) as seller_name, \
                    ifnull(avg(rating),0) as rating, item.mrp, (item.mrp-item.price)*100/item.mrp as discount FROM item \
                    INNER JOIN `category` ON (`item`.`category_id` = `category`.`id`)\
                    join user on item.seller_id = user.id\
                    left join review on item.id = review.item_id\
                    WHERE `category`.`name` = %s\
                    group by item.id\
                    ;',
                    [category],
                )
                queryset = cursor.fetchall()
        if search is not None:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT item.id, item.name, price, concat(user.first_name, ' ', user.last_name) as seller_name, \
                ifnull(avg(rating),0) as rating, item.mrp, (item.mrp-item.price)*100/item.mrp as discount FROM item \
                INNER JOIN `category` ON (`item`.`category_id` = `category`.`id`) \
                join user on item.seller_id = user.id\
                left join review on item.id = review.item_id\
                WHERE `category`.`name` LIKE %s\
                OR item.name LIKE %s\
                group by item.id\
                ;",
                    ["%" + search + "%", "%" + search + "%"],
                )
                queryset = cursor.fetchall()
        if trending is not None:
            with connection.cursor() as cursor:
                cursor.execute(
                    'SELECT item.id, item.name, item.price, concat(user.first_name, " ", user.last_name) as seller_name, \
                ifnull(avg(rating),0) as rating, item.mrp, (item.mrp-item.price)*100/item.mrp as discount FROM item \
                join user on item.seller_id = user.id\
                left join review on item.id = review.item_id\
                group by item.id\
                order by total_sale desc\
                limit %s;',
                    [int(trending)],
                )
                queryset = cursor.fetchall()

        data = []
        for item in queryset:
            data.append(
                {
                    "id": item[0],
                    "name": item[1],
                    "price": item[2],
                    "seller_name": item[3],
                    "rating": float(item[4]),
                    "mrp" : item[5],
                    "discount": float(item[6]),
                }
            )
        return data

    def get(self, request):
        data = self.get_data()
        return JsonResponse(data, safe=False)


class CategoryListAPI(APIView):
    permission_classes = []

    def get_data(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, name, image FROM category")
            queryset = cursor.fetchall()
        data = []
        for category in queryset:
            data.append(
                {
                    "id": category[0],
                    "name": category[1],
                    "image": category[2],
                }
            )
        return data

    def get(self, request):
        data = self.get_data()
        return JsonResponse(data, safe=False)


class ItemRetreiveAPI(APIView):
    permission_classes = []

    def get(self, request):
        id = self.request.query_params.get("id", None)
        if not id:
            raise CustomValidationError("Invalid request Parameters")

        with connection.cursor() as cursor:
            cursor.execute(
                'SELECT item.id, item.name, price, description, total_sale, concat(user.first_name, " ", user.last_name) as seller_name, \
            store_name, ifnull(avg(rating),0) as rating, item.mrp, (item.mrp-item.price)*100/item.mrp as discount FROM item \
            join user on item.seller_id = user.id\
            left join review on item.id = review.item_id\
            join seller on item.seller_id = seller.user_id\
            WHERE item.id = %s',
                [id],
            )
            queryset = cursor.fetchone()

        data = {
            "id": queryset[0],
            "name": queryset[1],
            "price": queryset[2],
            "description": queryset[3],
            "total_sale": queryset[4],
            "seller_name": queryset[5],
            "store_name": queryset[6],
            "rating": float(queryset[7]),
            "mrp" : queryset[8],
            'discount' : float(queryset[9]),
        }

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT group_concat(image) FROM itemimage WHERE item_id = %s", [
                    id]
            )
            queryset = cursor.fetchall()

        data["images"] = queryset[0][0].split(",") if queryset[0] else []

        with connection.cursor() as cursor:
            cursor.execute(
                'SELECT concat(user.first_name, " ", user.last_name) as name, message, rating, image, title FROM review\
            join `order` on review.order_id = `order`.id\
            join user on `order`.customer_id = user.id\
            WHERE item_id = %s',
                [id],
            )
            queryset = cursor.fetchall()

        reviews = []
        for review in queryset:
            reviews.append(
                {
                    "reviewer_name": review[0],
                    "description": review[1],
                    "rating": float(review[2]),
                    "image": review[3],
                    "title": review[4],
                }
            )
        data["reviews"] = reviews
        return JsonResponse(data)
