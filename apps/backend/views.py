from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseBadRequest

import requests
import datetime
import tempfile # used for downloader
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework import generics
from .models import Mooclet
from .serializers import MoocletSerializer

from mooclets.utils.mooclet_connector import MoocletConnector, MoocletCreator
from mooclets.utils import mooclet_connector
from mooclets.utils.DataPipelines.MoocletPipeline import MoocletPipeline


### USE THIS API TOKEN WITH CARE ###
MOOCLET_API_TOKEN = mooclet_connector.DUMMY_MOOCLET_API_TOKEN
URL = mooclet_connector.DUMMY_MOOCLET_URL


# call external api to create and get mooclet basic inof from IAI's MOOClet server
@api_view(('GET', 'POST'))
def process_mooclet(request):
    endpoint = "mooclet"
    if request.method == "GET":
        objects = requests.get(
            url = URL + endpoint + "/" + str(request.query_params.get('mooclet_id')),  # specify mooclet_id
            headers = {'Authorization': f'Token {MOOCLET_API_TOKEN}'},
            timeout=20
        )
        if objects.status_code != 200:
            print("unable to get mooclet")
        else:
            mooclet_data = objects.json()
            print("obtained mooclet data: ", mooclet_data)
            return Response(mooclet_data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        params = {"policy": int(str(request.query_params.get('policy_id'))),
                  "name": str(request.query_params.get('mooclet_name')) + str(datetime.datetime.now())}
        objects = requests.post(
            url = URL + endpoint,
            data = params,
            headers = {'Authorization': f'Token {MOOCLET_API_TOKEN}'},
            timeout=20
        )
        if objects.status_code != 201:
            print("unable to create mooclet")
        else:
            mooclet_data = objects.json()
            print("created mooclet in IAI's server: ", mooclet_data)
            # # TODO: write to DB
            # mooclet = Mooclet(
            #     study=...
            #     external_id=mooclet_data['id']
            #           )
            # mooclet.save()
            # print("new mooclet saved to django db")
            return Response(mooclet_data, status=status.HTTP_201_CREATED)


# call external api to create & get policy parameters for a given mooclet_id
@api_view(('GET', 'POST'))
def process_policy_parameters(request):
    url = URL
    token = MOOCLET_API_TOKEN
    try:
        mooclet_id = int(str(request.query_params.get('mooclet_id')))
    except (AttributeError, requests.HTTPError) as e:
        print("Error: gave wrong parameters: check mooclet_id")
        print(str(e))
        return HttpResponseBadRequest(e)

    try:
        mooclet_connector = MoocletConnector(mooclet_id=mooclet_id, token=token, url=url)
    except requests.HTTPError as e:
        return HttpResponseBadRequest(e)

    if request.method == "GET":  # given mooclet_id
        try:
            policy_params_data = mooclet_connector.get_policy_parameters()
            # TODO: add policy parameter field to Django model Mooclet() & seed here
            return Response(policy_params_data, status=status.HTTP_200_OK)
        except requests.HTTPError as e:
            return HttpResponseBadRequest(e)

    elif request.method == "POST":  # given mooclet_id and policy_id
        # pre-condition: the mooclet must have been created already
        try:
            policy_id = int(str(request.query_params.get('policy_id')))
            policy_parameters = request.query_params.get('policy_parameters')  # json string
        except (AttributeError, requests.HTTPError) as e:
            print("Error: gave wrong parameters: check policy_id or parameters")
            print(str(e))
        try:
            policy_params_object_created = mooclet_connector.create_policy_parameters(policy_id, policy_parameters)
            return Response(policy_params_object_created, status=status.HTTP_201_CREATED)
        except requests.HTTPError as e:
            return HttpResponseBadRequest(e)


# call external api to create & get variables and their values for a given mooclet_id
@api_view(('GET', 'POST'))
def process_variables(request):
    url = URL
    token = MOOCLET_API_TOKEN
    try:
        mooclet_id = int(str(request.query_params.get('mooclet_id')))
    except (AttributeError, requests.HTTPError) as e:
        print("Error: gave wrong parameters: check mooclet_id")
        print(str(e))
        return HttpResponseBadRequest(e)

    try:
        mooclet_connector = MoocletConnector(mooclet_id=mooclet_id, token=token, url=url)
    except requests.HTTPError as e:
        return HttpResponseBadRequest(e)

    if request.method == "GET":
        try:
            variables_values = mooclet_connector.get_values()
            return Response(variables_values, status=status.HTTP_200_OK)
        except requests.HTTPError as e:
            return HttpResponseBadRequest(e)

    elif request.method == "POST":
        try:
            variable_name = str(request.query_params.get('variable_name'))
        except (AttributeError, requests.HTTPError) as e:
            print("Error: gave wrong parameters: check variable_name or variable_value")
            print(str(e))
            return HttpResponseBadRequest(e)

        try:
            # create variable
            variable_created = mooclet_connector.create_variable(variable_name)
            temporary_value = mooclet_connector.create_value(variable_name)  # TODO: remove; don't manually create value
            return Response(variable_created, status=status.HTTP_201_CREATED)
        except requests.HTTPError as e:
            return HttpResponseBadRequest(e)


@api_view(('GET', 'POST'))
def process_versions(request):
    url = URL
    token = MOOCLET_API_TOKEN
    try:
        mooclet_id = int(str(request.query_params.get('mooclet_id')))
    except (AttributeError, requests.HTTPError) as e:
        print("Error: gave wrong parameters: check mooclet_id")
        print(str(e))
        return HttpResponseBadRequest(e)

    try:
        mooclet_connector = MoocletConnector(mooclet_id=mooclet_id, token=token, url=url)
    except requests.HTTPError as e:
        return HttpResponseBadRequest(e)

    if request.method == 'GET':
        try:
            versions = mooclet_connector.get_versions()
            return Response(versions, status=status.HTTP_200_OK)
        except requests.HTTPError as e:
            return HttpResponseBadRequest(e)
    elif request.method == 'POST':
        try:
            version_name = str(request.query_params.get('version_name'))
            version_json = request.query_params.get('version_json')  # json string
            version_text = str(request.query_params.get('version_text'))
        except (AttributeError, requests.HTTPError) as e:
            print("Error: gave wrong parameters: check version_name")
            return HttpResponseBadRequest(e)

        try:
            version_created = mooclet_connector.create_versions(version_name, version_json, version_text)
            return Response(version_created, status=status.HTTP_201_CREATED)
        except requests.HTTPError as e:
            return HttpResponseBadRequest(e)


def download_data(request):
    try:
        mooclet_id = str(request.query_params.get('mooclet_id'))
        var_names = str(request.query_params.get('var_names'))
        
    except (AttributeError, requests.HTTPError) as e:
        # NOTE: We eventually want to stop using this, but use for testing.
        print("Error: " + str(e))
        mooclet_id = 25
        var_names = {
            "reward": "mturk_ts_reward_round_8",
            "policy": 6
        }
        #return HttpResponseBadRequest(e)

    token = MOOCLET_API_TOKEN
    url = URL

    try:
        mooclet_connector = MoocletConnector(mooclet_id=mooclet_id, url=url, token=token)
    except requests.HTTPError as e:
        return HttpResponseBadRequest(e)

    tfile = tempfile.NamedTemporaryFile(mode="w+")

    a = MoocletPipeline(mooclet_connector, var_names)

    try:
        a.get_output(tfile)
    except requests.HTTPError as e:
        return HttpResponseBadRequest(e)

    filename = f"{mooclet_id}.csv"

    response = HttpResponse(tfile, content_type="text/csv")
    response['Content-Dispostion'] = "attachment; filename=%s" % filename

    return response


# list & create models
class MoocletCreate(generics.ListCreateAPIView):
    queryset = Mooclet.objects.all()
    serializer_class = MoocletSerializer
