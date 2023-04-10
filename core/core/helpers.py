from .exceptions import CustomValidationError


def check_keys(request: dict, keys: list):
    for key in keys:
        if key not in request.keys():
            raise CustomValidationError("Insufficient Data: " + str(key))
