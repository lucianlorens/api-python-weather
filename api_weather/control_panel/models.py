from django.db import models

class Location(models.Model):

    description = models.CharField(max_length=30)
    latitude = models.CharField(max_length=30)
    longitude = models.CharField(max_length=30)
    created_at = models.DateTimeField(blank=True)
    updated_at = models.DateTimeField(blank=True)
    parameters_url = models.TextField(blank=True)
    # aggregation = models.JSONField() # retrieved from parameters
    # details = models.JSONField() # retrieved from parameters

class Parameter(models.Model):
    name = models.CharField(max_length=30)
    climacell_type = models.CharField(max_length=30)
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)
    location_url = models.CharField(max_length=30)
    created_at = models.DateTimeField(blank=True)
    # measurement_unit = models.CharField(max_length=30) # retrieved by request
    # values = models.JSONField() #retrieved by request, filter by type
    # aggregation = models.JSONField() #retrieved by request, filter by type
    # details = models.JSONField()
    