# from rest_framework.compat import is_authenticated
from rest_framework.permissions import DjangoObjectPermissions, BasePermission


class SgsplPermission(DjangoObjectPermissions):
    """
    Custom Permission class for susthome
    """
    def has_permission(self, request, view):

        if request.user.is_superuser:
            return True

        super(SgsplPermission, self).has_permission(request, view)


class SgsplNoObjectPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff
