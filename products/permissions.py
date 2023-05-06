from rest_framework import permissions


class IsGetorSeller(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        else:
            return request.user.is_authenticated and request.user.is_seller


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return True
        else:
            if request.user.is_authenticated and request.user.is_seller:
                return request.user.id == obj.seller.id
            else:
                return False
