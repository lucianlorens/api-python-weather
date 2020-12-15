from django.db import models

class Location(models.Model):
    location_id = models.CharField=(max_length=50)
    description = models.CharField=(max_length=50) 
    parameters = models.CharField=(max_length=50)

    class Meta:
        verbose_name_plural = 'locations'
    
    def __str(self):
        return self.title