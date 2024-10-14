from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_admin

class IsHRUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_hr

class IsManagerUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_manager

class IsAdminOrHR(BasePermission):
    """
    Allows access if the user is admin or HR.
    """
    def has_permission(self, request, view):
        return (
            IsAdminUser().has_permission(request, view) or
            IsHRUser().has_permission(request, view)
        )
