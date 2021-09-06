"""
Define custom permissions and will be used to views.
"""
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsStaff(BasePermission):
    """Authenticate user if user is a staff."""
    message = "you're not a staff."

    def has_permission(self, request, view):
        return request.user.is_staff


class ReadOnly(BasePermission):
    """If not logged in, user only can read."""

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsOwnerOrStaff(BasePermission):
    """Object can be updated only by an user or staff."""
    message = "Object can be updated by owner or staff."

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user or request.user.is_staff
