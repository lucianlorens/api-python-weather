from django.contrib.auth.models import User, Group
from rest_framework import serializers
from api_weather.control_panel.models import Location, Parameter

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class ParameterSerializer(serializer.ModelSerializer):
    class Meta:
        model = Parameter
        fields = '__all__'