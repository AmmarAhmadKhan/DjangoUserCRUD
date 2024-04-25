from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to access or modify it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id


class IsUserOrganization(permissions.BasePermission):
    """
    Custom permission to only allow users of an organization to access or modify it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.organization.id
