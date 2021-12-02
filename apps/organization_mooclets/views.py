from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import action

from organizations.models import Organization
from mooclets.models import Mooclet
from .models import OrganizationMoocletAuthenticator

from .serializers import OrganizationMoocletSerializer, OrganizationExternalMoocletCreateSerializer, OrganizationMoocletCreateSerializer

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
            return OrganizationMoocletCreateSerializer
        elif self.action == 'create_external':
            return OrganizationExternalMoocletCreateSerializer
        else:
            return self.serializer_class

    def get_serializer_context(self):
        if self.action == 'create':
            return {"organization_pk": self.kwargs["organization_pk"]}
        else:
            return {}

    @action(detail=False, methods=['post'], name='Create External Mooclet')
    def create_external(self, request, organization_pk):
        organization = Organization.objects.get(pk=organization_pk)
        mooclet_authenticator = organization.mooclet_authenticator
        mooclet_creator = mooclet_authenticator.get_mooclet_creator()
        policy_id = request.data["policy_id"]
        mooclet_name = request.data["mooclet_name"]
        mooclet_data = mooclet_creator.create_mooclet(policy=policy_id, name=mooclet_name)
        Mooclet.objects.create(external_id=mooclet_data["id"], content_object=mooclet_authenticator)
        return Response(status=status.HTTP_201_CREATED)

