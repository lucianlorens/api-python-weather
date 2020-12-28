from django.shortcuts import render

from django.contrib.auth.models import User, Group

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from api_weather.control_panel.serializers import UserSerializer, GroupSerializer, LocationSerializer

from api_weather.control_panel.models import Location

from dotenv import load_dotenv
from pathlib import Path 

import json
from datetime import datetime

import handlers.climacell as climacell

import handlers.aggregation as aggregator

import requests


env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path, verbose=True)


@api_view(['GET', 'POST'])
def locations_list(request):
    if request.method == 'GET':
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        request.data['created_at'] = datetime.now() 
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH', 'DELETE'])
def locations_detail(request, pk):

    try:
        location = Location.objects.get(pk=pk)

    except Location.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        
        serializer = LocationSerializer(location)
        
        #### WIP
        parameters_url = serializer.data['parameters_url']
        
        parameters_response = requests.get(parameters_url)
        
        parameters_body_json = json.loads(parameters_response.text)

        parameters_dict = {}

        for parameter in parameters_body_json:
            parameters_dict[ parameter['name'] ] : parameter['climacell_type']

        latitude = location_serializer.data['latitude']
        longitude = location_serializer.data['longitude']

        climacell_data = climacell.get_climacell_data(latitude, longitude, parameters_type_list)

        aggregation_dict = {}
        for key in parameters_dict.keys():
            aggregation_dict[key].append( aggregator.metric_aggregation(key, parameters_dict[key], climacell_data) )

        serializer.data['Aggregation'] = aggregation_dict
        
        return Response(serializer.data)

    elif request.method == 'PATCH':
        request.data['updated_at'] = datetime.now() 
        serializer = LocationSerializer(location, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        location.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


###########################################################################


@api_view(['GET', 'POST'])
def parameters_list(request, location_pk):
    if request.method == 'GET':
        parameters = Parameter.objects.get(location_id=location_pk)
        serializer = ParameterSerializer(parameters, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        request.data['created_at'] = datetime.now() 
        serializer = ParameterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
def parameters_detail(request, location_pk, parameter_pk):

    try:
        parameter = Parameter.objects.get(pk=parameter_pk)
        location = Location.objects.get(pk=location_pk)

    except Parameter.DoesNotExist, Location.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        parameter_serializer = ParameterSerializer(parameter)
        location_serializer = LocationSerializer(location)
        
        latitude = location_serializer.data['latitude']
        longitude = location_serializer.data['longitude']
        metric_type = parameter_serializer.data['climacell_type']
        
        climacell_data = climacell.get_climacell_data(latitude, longitude, metric_type)
        
        metric_name = parameter_serializer.data['name']
        parameter_aggregation = aggregator.metric_aggregation(metric_name, metric_type, climacell_data)

        parameter_serializer.data['aggregation'] = parameter_aggregation
        parameter_serializer.data['values'] = climacell_data

        return Response(parameter_serializer.data)

    elif request.method == 'DELETE':
        parameter.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


###########################################################################




class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]