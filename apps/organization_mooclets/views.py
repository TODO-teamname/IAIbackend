from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from organizations.models import Organization
from mooclets.models import Mooclet

from .models import OrganizationMoocletAuthenticator
from .serializers import OrganizationMoocletSerializer
from .permissions import OrganizationMoocletPermissions


class OrganizationMoocletViewSet(mixins.CreateModelMixin,
                                 mixins.ListModelMixin,
                                 viewsets.GenericViewSet):

    queryset = Mooclet.objects.all()
    permission_classes = [IsAuthenticated, OrganizationMoocletPermissions]
    serializer_classes = OrganizationMoocletSerializer

    def get_queryset(self):
        organization = Organization.objects.get(id = self.kwargs['organization_pk'])
        return Mooclet.objects.filter(authenticator_id=organization.authenticator_id)

    def perform_create(self, serializer):
        organization = Organization.objects.get(id = self.kwargs['organization_pk'])
        try:
            authenticator = OrganizationMoocletAuthenticator.objects.get(organization=organization)
        except:
            authenticator = OrganizationMoocletAuthenticator(organization = organization)
            authenticator.save()
        serializer.save()

    """
    @action(detail=False)
    def create_external(self):
        pass
    """
