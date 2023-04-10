from rest_framework import permissions


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
