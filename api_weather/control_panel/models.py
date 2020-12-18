from django.db import models

class Location(models.Model):
    description = models.CharField(max_length=30)
    parameters = models.CharField(max_length=30)
    aggregation = models.JSONField()
    details = models.JSONField()

class Parameter(models.Model):
    name = models.CharField(max_length=30)
    location = models.CharField(max_length=30)
    measurement_unit = models.CharField(max_length=30)
    values = models.JSONField()
    aggregation = models.JSONField()
    details = models.JSONField()
