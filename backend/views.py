from django.shortcuts import render

import requests
import datetime
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from .models import Mooclet
from .serializers import MoocletSerializer
from rest_framework import generics

### USE THIS API WITH CARE ###
MOOCLET_API_TOKEN = "db071db130485666bfd39ac15b9dc1eb9d75f9cc"
URL = "https://mooclet.canadacentral.cloudapp.azure.com/engine/api/v1/"

# POLICY_NAME_TO_ID = {"thompson_sampling_contextual": 6, 
#                      "choose_policy_group": 12,
#                      "ts_configurable": 17}


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
            mooclet_data = objects.json()  # mooclet #25 retured
            print("obtained mooclet data: ", mooclet_data)
            # seed to Django DB
            mooclet = Mooclet(mooclet_name=mooclet_data['name'], 
                              mooclet_id=mooclet_data['id'], 
                              policy_id=mooclet_data['policy'],
                      )
            mooclet.save()
            print("mooclet saved to django db")
            
            return Response(mooclet_data, status=status.HTTP_200_OK, headers={'Access-Control-Allow-Origin': 'http://localhost:3000'})

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
            mooclet_data = objects.json()  # mooclet #25 retured
            print("created mooclet in IAI's server: ", mooclet_data)
            # seed to Django DB
            mooclet = Mooclet(mooclet_name=mooclet_data['name'], 
                              mooclet_id=mooclet_data['id'], 
                              policy_id=mooclet_data['policy'],
                      )
            mooclet.save()
            print("new mooclet saved to django db")
            return Response(mooclet_data, status=status.HTTP_201_CREATED, headers={'Access-Control-Allow-Origin': 'http://localhost:3000'})



class MoocletCreate(generics.ListCreateAPIView):  # list & create models
    queryset = Mooclet.objects.all()
    serializer_class = MoocletSerializer