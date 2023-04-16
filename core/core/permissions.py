from rest_framework import permissions
from django.db import connection

class SellerPermission(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        auth = super().has_permission(request, view)
        return not not (auth and request.user.seller)


class CustomerPermission(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        auth = super().has_permission(request, view)
        return not not (auth and request.user.customer)
    

class IsOwnerOrReadOnly(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class IsAuthenticatedByID(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.META.get('HTTP_USER_ID'):
            return False
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM user WHERE id =%s", 
                [int(request.META['HTTP_USER_ID'])]
            )
            return not not cursor.fetchone()
