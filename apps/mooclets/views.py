from django.http.response import HttpResponse, HttpResponseBadRequest
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

import requests
import datetime
import tempfile # used for downloader
from rest_framework import status, generics, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from mooclets.models import Mooclet
from mooclets.serializers import MoocletSerializer, VersionSerializer, PolicyParameterSerializer, VariableSerializer, DownloadVarNamesSerializer

from mooclets.utils.mooclet_connector import MoocletConnector, MoocletCreator
from mooclets.utils.DataPipelines.MoocletPipeline import MoocletPipeline

class MoocletViewSet(generics.RetrieveAPIView,
                     viewsets.GenericViewSet):
    queryset = Mooclet.objects.all()
    serializer_class = MoocletSerializer

    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        permission_set = set(self.permission_classes)

        if self.detail == True:
            try:
                mooclet = Mooclet.objects.get(pk=self.kwargs['pk'])
            except ObjectDoesNotExist:
                raise Http404
            mooclet_permissions = mooclet.get_permission_classes()
            permission_set |= set(mooclet_permissions)

        return [permission() for permission in permission_set]
    
    def _get_helper(self, connector_method):
        mooclet = self.get_object()

        response_json = connector_method(mooclet.get_connector())

        return Response(response_json, status=status.HTTP_200_OK)

    def _update_helper(self, call_serializer, connector_method):
        mooclet = self.get_object()

        serializer = call_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        try:
            response_json = connector_method(mooclet.get_connector(), **serializer.validated_data)
        except requests.HTTPError as e:
            if e.response.status_code == 400:
                return Response(e.response.json(), status=status.HTTP_400_BAD_REQUEST)
            raise

        return Response(response_json, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def policyparameters(self, request, pk=None):
        return self._get_helper(connector_method=MoocletConnector.get_policy_parameters)

    @action(detail=True, methods=['get'])
    def variables(self, request, pk=None):
        return self._get_helper(connector_method=MoocletConnector.get_values)

    @action(detail=True, methods=['get'])
    def versions(self, request, pk=None):
        return self._get_helper(connector_method=MoocletConnector.get_versions)

    @variables.mapping.post
    def update_variables(self, request, pk=None):
        return self._update_helper(call_serializer=VariableSerializer, 
                                   connector_method=MoocletConnector.create_variable)

    @policyparameters.mapping.post
    def update_policyparameters(self, request, pk=None):
        return self._update_helper(call_serializer=PolicyParameterSerializer, 
                                   connector_method=MoocletConnector.create_policy_parameters)

    @versions.mapping.post
    def update_versions(self, request, pk=None):
        return self._update_helper(call_serializer=VersionSerializer, 
                                   connector_method=MoocletConnector.create_versions)

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        mooclet = self.get_object()
        mooclet_connector = mooclet.get_connector()

        #var_names = eval(request.query_params.get('var_names'))
        var_names = {"reward": "mturk_ts_reward_round_8", "policy": 6}
        serializer = DownloadVarNamesSerializer(data=var_names)
        serializer.is_valid(raise_exception=True)

        tfile = tempfile.NamedTemporaryFile(mode="w+")

        a = MoocletPipeline(mooclet_connector, var_names)

        try:
            a.get_output(tfile)
        except requests.HTTPError as e:
            return HttpResponseBadRequest(e)

        filename = f"{mooclet.name}.csv"

        response = HttpResponse(tfile, content_type="text/csv")
        response['Content-Dispostion'] = "attachment; filename=%s" % filename

        return response

