from django.db import models


class Location(models.Model):
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255, blank=True, null=True)
    building = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        unique_together = ("city", "street", "building", "country", "postal_code")

    def __str__(self):
        address_parts = [self.city, self.street, self.building, self.country, self.postal_code]
        return ", ".join(filter(None, address_parts))
