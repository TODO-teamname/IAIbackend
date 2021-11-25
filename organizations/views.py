from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from organizations.models import Organization, Membership
from organizations.serializers import OrganizationSerializer, MembershipSerializer
from organizations.permissions import OrganizationPermissions, MembershipPermissions

# Create your views here.
class OrganizationViewSet(mixins.ListModelMixin,
                          mixins.CreateModelMixin,
                          mixins.UpdateModelMixin,
                          viewsets.GenericViewSet):

    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [OrganizationPermissions]

    def get_queryset(self):
        return Organization.objects.filter(members=self.request.user)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class MembersViewSet(mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):

    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer
    permission_classes = [MembershipPermissions]

    def get_queryset(self):
        return Membership.objects.filter(organization=self.kwargs['organization_pk'])

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), user=self.kwargs['pk'])
        self.check_object_permissions(self.request.user, obj)
        return obj


    




