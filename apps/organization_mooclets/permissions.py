from rest_framework import permissions
from django.shortcuts import get_object_or_404

from organizations.models import Organization
from organizations.permissions import is_member, is_admin

class OrganizationMoocletPermissions(permissions.BasePermission):
    view_methods = ("GET", "HEAD")
    edit_methods = ("POST", "PUT", "PATCH", "DELETE")

    def has_permission(self, request, view):
        user = request.user
        organization = get_object_or_404(Organization, pk=view.kwargs["organization_pk"])

        if is_admin(user, organization):
            return True

        elif is_member(user, organization):
            return request.method in self.view_methods

        return False

    def has_object_permission(self, request, view, obj):
        user = request.user

        organization = obj.content_object.organization

        if is_admin(user, organization):
            return True

        elif is_member(user, organization):
            return request.method in self.view_methods

        return False

class OrganizationExternalMoocletPermissions(permissions.BasePermission):
    view_methods = ("GET", "HEAD")
    edit_methods = ("POST", "PUT", "PATCH")

    def has_object_permission(self, request, view, obj):
        user = request.user

        organization = obj.content_object.organization

        if is_admin(user, organization):
            return True

        elif is_member(user, organization):
            return request.method in self.view_methods

        return False
