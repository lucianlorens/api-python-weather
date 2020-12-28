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


env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path, verbose=True)


@api_view(['GET', 'POST'])
def locations_list(request):
    if request.method == 'GET':
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        request.data.update( { 'created_at':datetime.now() } )
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
        # TODO: add climacell data
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
        request.data['updated_at'] = datetime.now() 
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
        serializer = ParameterSerializer(parameter)
        # TODO: add climacell data
        return Response(serializer.data)

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