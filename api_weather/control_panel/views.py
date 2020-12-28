from django.shortcuts import render

from django.contrib.auth.models import User, Group

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from api_weather.control_panel.serializers import UserSerializer, GroupSerializer, LocationSerializer, ParameterSerializer
from api_weather.control_panel.models import Location, Parameter

import api_weather.control_panel.handlers.climacell as climacell
import api_weather.control_panel.handlers.aggregation as aggregator

import requests
import json
from datetime import datetime


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
        
        location_serializer = LocationSerializer(location)
        
        parameters_url = location_serializer.data['parameters_url']
        
        parameters_response = requests.get("http://"+parameters_url)
        
        parameters_body_json = json.loads(parameters_response.text)

        latitude = location_serializer.data['latitude']
        longitude = location_serializer.data['longitude']

        parameters_type_list = [i["climacell_type"] for i in parameters_body_json]

        climacell_data = climacell.get_climacell_data(latitude, longitude, parameters_type_list)

        aggregation_list = []

        for parameter in parameters_body_json:
            aggregation_list.append( aggregator.metric_aggregation(parameter["name"], parameter["climacell_type"], climacell_data) )

        location_response = location_serializer.data

        location_response.update({
        "aggregation" : aggregation_list
        })

        return Response(location_response)

    elif request.method == 'PATCH':
        request.data['updated_at'] = datetime.now() 
        location_serializer = LocationSerializer(location, data=request.data)

        if location_serializer.is_valid():
            location_serializer.save()
            return Response(location_serializer.data)

        return Response(location_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        location.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


###########################################################################


@api_view(['GET', 'POST'])
def parameters_list(request, location_pk):
    
    if request.method == 'GET':
        try:
            parameters = Parameter.objects.filter(location_id=location_pk)
            serializer = ParameterSerializer(parameters, many=True)
            return Response(serializer.data)
        except Parameter.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'POST':
        request.data['created_at'] = datetime.now()
        request.data['location_id'] = location_pk
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

    except (Parameter.DoesNotExist, Location.DoesNotExist):
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        parameter_serializer = ParameterSerializer(parameter)
        location_serializer = LocationSerializer(location)
        
        latitude = location_serializer.data['latitude']
        longitude = location_serializer.data['longitude']

        metric_type = parameter_serializer.data['climacell_type']
        
        climacell_data = climacell.get_climacell_data(latitude, longitude, metric_type )
        
        metric_name = parameter_serializer.data['name']
        parameter_aggregation = aggregator.metric_aggregation(metric_name, metric_type, climacell_data)

        parameter_response = parameter_serializer.data

        parameter_response.update({
        "aggregation" : parameter_aggregation,
        "values" : climacell_data
        })

        return Response(parameter_response)

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