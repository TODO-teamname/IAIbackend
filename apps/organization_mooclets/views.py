from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import action

from organizations.models import Organization
from mooclets.models import Mooclet
from .models import OrganizationMoocletAuthenticator

from .serializers import OrganizationMoocletSerializer, CreateOrganizationMoocletSerializer
from .permissions import OrganizationMoocletPermissions


class OrganizationMoocletViewSet(mixins.CreateModelMixin,
                                 mixins.ListModelMixin,
                                 mixins.RetrieveModelMixin,
                                 mixins.DestroyModelMixin,
                                 viewsets.GenericViewSet):

    queryset = Mooclet.objects.all()
    permission_classes = [IsAuthenticated, OrganizationMoocletPermissions]
    serializer_class = OrganizationMoocletSerializer

    def get_queryset(self):
        organization = Organization.objects.get(id = self.kwargs['organization_pk'])

        try:
            mooclet_authenticator = OrganizationMoocletAuthenticator.objects.get(organization=organization)
        except ObjectDoesNotExist:
            OrganizationMoocletAuthenticator.objects.create(organization=organization)

        mooclet_authenticator = organization.mooclet_authenticator
        content_type =ContentType.objects.get_for_model(mooclet_authenticator)
        return Mooclet.objects.filter(object_id=mooclet_authenticator.id, content_type = content_type)

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateOrganizationMoocletSerializer
        else:
            return self.serializer_class

    def get_serializer_context(self):
        if self.action == 'create':
            return {"organization_pk": self.kwargs["organization_pk"]}
        else:
            return {}

    """
    @action(detail=False)
    def create_external(self):
        pass
    """
