from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from organizations.models import Organization, Membership
from organizations.serializers import OrganizationSerializer, MembershipSerializer
from organizations.permissions import OrganizationPermissions, MembershipPermissions

# Create your views here.
class OrganizationViewSet(mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.CreateModelMixin,
                          mixins.UpdateModelMixin,
                          viewsets.GenericViewSet):

    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated, OrganizationPermissions]

    def get_queryset(self):
        return Organization.objects.filter(members=self.request.user)

class MembersViewSet(mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):

    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer
    permission_classes = [IsAuthenticated, MembershipPermissions]

    def get_queryset(self):
        return Membership.objects.filter(organization_id=self.kwargs['organization_pk'])

    def perform_create(self, serializer):
        serializer.save(organization_id=self.kwargs['organization_pk'])
