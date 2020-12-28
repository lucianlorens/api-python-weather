from django.db import models

class Location(models.Model):

    description = models.CharField(max_length=30)
    latitude = models.CharField(max_length=30)
    longitude = models.CharField(max_length=30)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    parameters_url = models.CharField(max_length=254, blank=True, null=True)
    
class Parameter(models.Model):
    name = models.CharField(max_length=30)
    climacell_type = models.CharField(max_length=30)
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)
    location_url = models.CharField(max_length=254)
    created_at = models.DateTimeField(blank=True, null=True)
    