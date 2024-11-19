from django.utils import timezone
from django.db import models

class Alumni(models.Model):
    full_name = models.CharField(max_length=255,default="Full Name")
    university_affiliation = models.TextField(default="Unknown University")  # Added default value
    date_of_death = models.DateField(null=True, blank=True)
    obituary_url = models.URLField(max_length=500, null=True, blank=True)
    family_info = models.TextField(null=True, blank=True)
    funeral_details = models.TextField(null=True, blank=True)
    notable_info = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.full_name