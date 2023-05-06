from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return True
        else:
            return request.user.is_authenticated and request.user.id == obj.id
