from rest_framework import permissions

from .models import Organization, Membership, PERMISSION_LEVELS

class OrganizationPermissions(permissions.BasePermission):
    safe_methods = ("POST", "GET")
    view_methods = ("HEAD")
    edit_methods = ("PUT", "PATCH")

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.is_superuser:
            return True

        try:
            membership = Membership.objects.get(person=user, organization = obj)
        except:
            return False

        if request.method in self.view_methods:
            return True

        if membership.permissions == "ADMIN":
            return True

        return False

class MembershipPermissions(OrganizationPermissions):
    safe_methods = ("POST", "GET")
    view_methods = ("HEAD")
    edit_methods = ("PUT", "PATCH")

    def has_permission(self, request, view):
        # TODO: figure out permissions!!!
        organization = Organization.objects.get(pk=view.kwargs["organization_pk"])
        org_permissions = OrganizationPermissions()

        if org_permissions.has_object_permission(request, view, organization):
            if request.method != "ADMIN":
                return True
        return False

    def has_object_permission(self, request, view, obj):
        organization = Organization.objects.get(pk=view.kwargs["organization_pk"])
        org_permissions = OrganizationPermissions()

        if org_permissions.has_object_permission(request, view, organization):
            if obj.permission_level != "ADMIN":
                return True

        user = request.user

        if obj.user == user and request.method == "DELETE":
            return True

        return False



