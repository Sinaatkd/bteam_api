from rest_framework.permissions import BasePermission


class IsAccountOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user.id == obj.id)


class IsTransactionOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user.id == obj.user.id)


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.is_staff)
