from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Allow safe methods for everyone, but only allow authors to edit/delete.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions for anyone (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True
        # For write permissions, only the author can edit/delete
        return getattr(obj, 'author', None) == request.user
