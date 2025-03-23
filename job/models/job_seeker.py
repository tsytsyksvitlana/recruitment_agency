from django.db import models


class JobSeeker(models.Model):
    user = models.OneToOneField(
        'authenticate.User', on_delete=models.CASCADE, related_name="jobseeker_profile"
    )
