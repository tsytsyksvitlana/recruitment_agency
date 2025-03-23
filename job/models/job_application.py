from django.db import models


class JobApplication(models.Model):
    job_seeker = models.ForeignKey('job.JobSeeker', on_delete=models.CASCADE, related_name="applications")
    vacancy = models.ForeignKey('job.JobVacancy', on_delete=models.CASCADE, related_name="applications")
    cover_letter = models.TextField(blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)
