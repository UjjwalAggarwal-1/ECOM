from rest_framework import status
from rest_framework.exceptions import APIException


class CustomValidationError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Server error occurred"

    def __init__(self, detail, status_code=status.HTTP_400_BAD_REQUEST):
        if status_code is not None:
            self.status_code = status_code
        if detail is not None:
            self.detail = detail
        else:
            self.detail = self.default_detail
