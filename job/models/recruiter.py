from django.db import models


class Recruiter(models.Model):
    user = models.OneToOneField('authenticate.User', on_delete=models.CASCADE, related_name="recruiter_profile")
    company = models.ForeignKey('job.Company', on_delete=models.SET_NULL, null=True, blank=True)
