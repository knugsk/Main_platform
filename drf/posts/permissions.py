from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsStaffOrAdminWriteOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True  # Allow read-only permissions for all users
        return request.user.is_staff or request.user.is_superuser

class IsAuthorOrStaffOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True  # Allow read-only permissions for all users

        # Check if the user is the author of the object
        if obj.author == request.user:
            return True

        # Check if the user is staff or admin
        return request.user.is_staff or request.user.is_superuser
