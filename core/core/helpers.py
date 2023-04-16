from .exceptions import CustomValidationError
from django.db import connection

def check_keys(request: dict, keys: list):
    for key in keys:
        if key not in request.keys():
            raise CustomValidationError("Insufficient Data: " + str(key))


def get_user_from_request(request):
    if "HTTP_USER_ID" not in request.META.keys():
        raise CustomValidationError("Invalid Request")
    
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT id, id, email, first_name, last_name, mobile, age, sex FROM user WHERE id =%s", 
            [int(request.META['HTTP_USER_ID'])]
        )
        user = cursor.fetchone()
        if not user:
            raise CustomValidationError("Invalid User Request")
        
    user_data = {
        "id": user[0],
        # "id": user[1],
        "email": user[2],
        "first_name": user[3],
        "last_name": user[4],
        "mobile": user[5],
        "age": user[6],
        'sex': user[7]
    }
    
    return user_data