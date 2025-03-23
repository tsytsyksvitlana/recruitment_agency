from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    location = models.ForeignKey('job.Location', on_delete=models.SET_NULL, null=True, blank=True, related_name="companies")

    def __str__(self):
        return self.name
