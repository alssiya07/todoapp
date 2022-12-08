from rest_framework import permissions

class IsOwnerPermission(permissions.BasePermission):
    message="you have no permission"

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return request.user==obj.user