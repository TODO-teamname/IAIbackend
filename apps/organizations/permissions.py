from rest_framework import permissions

from .models import Organization, Membership

def is_member(user, organization):
    try:
        Membership.objects.get(user=user, organization=organization.id)
    except:
        return False

    return True

def is_admin(user, organization):
    try:
        membership = Membership.objects.get(user=user, organization=organization.id)
    except:
        return False

    return membership.permission_level == "ADMIN"

class OrganizationPermissions(permissions.BasePermission):
    safe_methods = ()
    view_methods = ("HEAD", "GET")
    edit_methods = ("PUT", "PATCH")

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.is_superuser:
            return True

        if request.method in self.safe_methods:
            return True

        if is_member(user, obj) and request.method in self.view_methods:
            return True

        if is_admin(user, obj):
            return True

        return False

class MembershipPermissions(permissions.BasePermission):
    view_methods = ("GET", "HEAD")
    edit_methods = ("POST", "PUT", "PATCH")

    def has_permission(self, request, view):
        user = request.user
        organization = Organization.objects.get(pk=view.kwargs["organization_pk"])

        if is_admin(user, organization):
            return True

        elif is_member(user, organization):
            if request.method in self.view_methods or request.method == "DELETE":
                return True

        return False

    def has_object_permission(self, request, view, obj):
        user = request.user

        organization = obj.organization

        if user.is_superuser:
            return True

        if is_admin(user, organization):
            # an admin can only remove themselves or demote themselves, unless they are the last admin.
            if obj.user == user: 
                if request.method == "DELETE" or (request.method == "PATCH" and request.data["permission_level"] != "ADMIN"):
                    self.message = {"user": "There must be at least one administrator in this organization."}
                    return organization.membership_set.filter(permission_level = "ADMIN").count() > 1

            # an admin cannot remove/modify other admins
            else: 
                return obj.permission_level != "ADMIN"
        elif is_member(user, organization):
            # a regular user should be able to leave an organization
            if obj.user == user and request.method == "DELETE":
                return True

            if request.method in self.view_methods:
                return True

        return False
