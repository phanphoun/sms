"""
Custom Permissions for Role-Based Access Control
"""
from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    Permission check for Admin role
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_admin()


class IsTeacher(permissions.BasePermission):
    """
    Permission check for Teacher role
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_teacher()


class IsStudent(permissions.BasePermission):
    """
    Permission check for Student role
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_student()


class IsAdminOrTeacher(permissions.BasePermission):
    """
    Permission check for Admin or Teacher roles
    """
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            (request.user.is_admin() or request.user.is_teacher())
        )


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Permission check: Object owner or Admin
    """
    def has_object_permission(self, request, view, obj):
        # Admin has full access
        if request.user.is_admin():
            return True
        
        # Check if obj has a user attribute
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        # Check if obj is the user themselves
        return obj == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Admin can edit, others can only read
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_authenticated and request.user.is_admin()
