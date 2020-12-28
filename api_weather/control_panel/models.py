from django.db import models

class Location(models.Model):
    
    description = models.CharField(max_length=30)
    parameters_urls = models.CharField(max_length=30, blank=True)
    #aggregation = models.JSONField() #going to be added during request
    # details = models.JSONField() #going to be added during request
    created_at = models.DateTimeField(blank=True)
    updated_at = models.DateTimeField(blank=True)

class Parameter(models.Model):
    name = models.CharField(max_length=30)
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)
    location_url = models.CharField(max_length=30)
    measurement_unit = models.CharField(max_length=30)
    values = models.JSONField()
    aggregation = models.JSONField()
    details = models.JSONField()
    created_at = models.DateTimeField()