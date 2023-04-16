from rest_framework.views import APIView
from rest_framework.response import Response
from core.exceptions import CustomValidationError
from core.helpers import check_keys
from core.permissions import IsAuthenticatedByID
from django.db import connection
from django.http.response import JsonResponse


class ItemListAPI(APIView):

    permission_classes = []
    fields = ("id", "name", "price",)

    def get_data(self):
        with connection.cursor() as cursor:
            cursor.execute(
            'SELECT item.id, item.name, item.price, concat(user.first_name, " ", user.last_name) as seller_name, \
            avg(rating) as rating FROM item \
            join user on item.seller_id = user.id\
            left join review on item.id = review.item_id\
            group by item.id\
            ;'
            )
            queryset = cursor.fetchall()

        category = self.request.query_params.get('category', None)
        search = self.request.query_params.get('search', None)
        trending = self.request.query_params.get('trending', None)
        
        if category is not None:
            with connection.cursor() as cursor:
                cursor.execute(
                    'SELECT item.id, item.name, price, concat(user.first_name, " ", user.last_name) as seller_name, \
                    avg(rating) as rating FROM item \
                    INNER JOIN `category` ON (`item`.`category_id` = `category`.`id`)\
                    join user on item.seller_id = user.id\
                    left join review on item.id = review.item_id\
                    WHERE `category`.`name` = %s\
                    group by item.id\
                    ;', 
                    [category]
                )
                queryset = cursor.fetchall()    
        if search is not None:
            with connection.cursor() as cursor:
                cursor.execute(
                "SELECT item.id, item.name, price, concat(user.first_name, ' ', user.last_name) as seller_name, \
                avg(rating) as rating FROM item \
                INNER JOIN `category` ON (`item`.`category_id` = `category`.`id`) \
                join user on item.seller_id = user.id\
                left join review on item.id = review.item_id\
                WHERE `category`.`name` LIKE %s\
                OR item.name LIKE %s\
                group by item.id\
                ;", 
                ['%'+search+'%', '%'+search+'%'] 
                )
                queryset = cursor.fetchall()    
        if trending is not None:
            with connection.cursor() as cursor:
                cursor.execute(
                'SELECT item.id, item.name, item.price, concat(user.first_name, " ", user.last_name) as seller_name, \
                avg(rating) as rating FROM item \
                join user on item.seller_id = user.id\
                left join review on item.id = review.item_id\
                group by item.id\
                order by total_sale desc\
                limit %s;',
                [int(trending)]
                )
                queryset = cursor.fetchall()    

        data = []
        for item in queryset:
            data.append({
                "id": item[0],
                "name": item[1],
                "price": item[2],
                "seller_name": item[3],
                "rating": item[4],
            })
        return data
    
    def get(self, request):
        data = self.get_data()
        return JsonResponse({'data':data})


class CategoryListAPI(APIView):
    permission_classes = []
    
    def get_data(self):
        with connection.cursor() as cursor:
            cursor.execute(
            'SELECT id, name, image FROM category'
            )
            queryset = cursor.fetchall()    
        data = []
        for category in queryset:
            data.append({
                "id": category[0],
                "name": category[1],
                "image": category[2],
            })
        return data

    
    def get(self, request):
        data = self.get_data()
        return JsonResponse({'data':data})


class ItemRetreiveAPI(APIView):
    permission_classes = []


    def get(self, request):
        id = self.request.query_params.get('id', None)
        if not id:
            raise CustomValidationError("Invalid request Parameters")
        
        with connection.cursor() as cursor:
            cursor.execute(
            'SELECT id, name, price, description, total_sale FROM item WHERE id = %s',
            [id]
            )
            queryset = cursor.fetchone()
        
        data = {
            "id": queryset[0],
            "name": queryset[1],
            "price": queryset[2],
            "description": queryset[3],
            "total_sale": queryset[4],
        }
        return JsonResponse({'data':data})