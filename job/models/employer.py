from django.db import models


class Employer(models.Model):
    user = models.OneToOneField('authenticate.User', on_delete=models.CASCADE, related_name='employer_profile')
    company = models.ForeignKey('job.Company', on_delete=models.CASCADE, related_name='employers', null=True)

    def __str__(self):
        return f"Employer {self.user.email} at {self.company.name}"
