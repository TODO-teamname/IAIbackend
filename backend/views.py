from django.shortcuts import render
import mimetypes
import os
import json
from django.http.response import HttpResponse, HttpResponseBadRequest

import requests
import datetime
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework import generics
from .models import Mooclet
from .serializers import MoocletSerializer
import tempfile # used for downloader

from .mooclet_connector import MoocletConnector, MoocletCreator
from . import mooclet_connector

### USE THIS API TOKEN WITH CARE ###
MOOCLET_API_TOKEN = mooclet_connector.DUMMY_MOOCLET_API_TOKEN
URL = mooclet_connector.DUMMY_MOOCLET_URL

RES_FRONTEND_HEADERS = {'Access-Control-Allow-Origin': 'http://localhost:3000'}


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
            # seed to Django DB
            mooclet = Mooclet(mooclet_name=mooclet_data['name'], 
                              mooclet_id=mooclet_data['id'], 
                              policy_id=mooclet_data['policy'],
                      )
            mooclet.save()
            print("mooclet saved to django db")
            
            return Response(mooclet_data, status=status.HTTP_200_OK, headers=RES_FRONTEND_HEADERS)

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
            # seed to Django DB
            mooclet = Mooclet(mooclet_name=mooclet_data['name'], 
                              mooclet_id=mooclet_data['id'], 
                              policy_id=mooclet_data['policy'],
                      )
            mooclet.save()
            print("new mooclet saved to django db")
            return Response(mooclet_data, status=status.HTTP_201_CREATED, headers=RES_FRONTEND_HEADERS)


# call external api to create & get policy parameters for a given mooclet_id
@api_view(('GET', 'POST'))
def process_policy_parameters(request):
    mooclet_id = int(str(request.query_params.get('mooclet_id')))
    url = URL
    token = MOOCLET_API_TOKEN
    mooclet_connector = MoocletConnector(mooclet_id=mooclet_id, token=token, url=url)

    if request.method == "GET":
        policy_params_data = mooclet_connector.get_policy_parameters()
        # TODO: add policy parameter field to Django model Mooclet() & seed here
        return Response(policy_params_data, status=status.HTTP_200_OK, headers=RES_FRONTEND_HEADERS)
    elif request.method == "POST":  # TODO: also requires specifying policy params in POST req
        # pre-condition: the mooclet must have been created already
        policy_id = mooclet_connector.get_mooclet()["policy"]
        parameters = {
            "policy_options": {
                "uniform_random": 0.0,
                "thompson_sampling_contextual": 1.0
            }
        }
        policy_params_object_created = mooclet_connector.create_policy_parameters(policy_id, parameters)
        # TODO: add policy parameter field to Django model Mooclet() & seed here
        return Response(policy_params_object_created, status=status.HTTP_201_CREATED, headers=RES_FRONTEND_HEADERS)


def download_data(request):
    #TODO: Reformat file
    try:
        mooclet_id = str(request.query_params.get('mooclet_id'))
        token = str(request.query_params.get('mooclet_token'))
        url = str(request.query_params.get('mooclet_url'))
    except (AttributeError, requests.HTTPError) as e:
        # NOTE: We eventually want to stop using this, but use for testing.
        print("Error: " + str(e))
        print("Using dummy values")
        mooclet_id = 25
        token = MOOCLET_API_TOKEN
        url = URL
        #return HttpResponseBadRequest(e)


    try:
        mooclet_connector = MoocletConnector(mooclet_id=mooclet_id, url=url, token=token)
        data = mooclet_connector.get_values()
    except requests.HTTPError as e:
        return HttpResponseBadRequest(e)

    tfile = tempfile.NamedTemporaryFile(mode="w+")

    json.dump(data, tfile)

    tfile.flush()
    tfile.seek(0)

    now = datetime.datetime.now()
    filename = f"{now}.csv"

    response = HttpResponse(tfile, content_type="text/csv")
    response['Content-Dispostion'] = "attachment; filename=%s" % filename

    return response


# list & create models
class MoocletCreate(generics.ListCreateAPIView):
    queryset = Mooclet.objects.all()
    serializer_class = MoocletSerializer
