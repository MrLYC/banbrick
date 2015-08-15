from rest_framework import permissions


class NoAnonymousUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return not request.user.is_authenticated()
