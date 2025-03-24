from django.db import models

from authenticate.models import User


class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employer_profile')
    company = models.ForeignKey('job.Company', on_delete=models.CASCADE, related_name='employers')

    def __str__(self):
        return f"Employer {self.user.email} at {self.company.name}"
