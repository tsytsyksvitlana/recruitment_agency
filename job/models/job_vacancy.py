from django.db import models


class JobVacancy(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    company = models.ForeignKey('job.Company', on_delete=models.CASCADE, related_name="vacancies")
    location = models.ForeignKey('job.Location', on_delete=models.SET_NULL, null=True, blank=True, related_name="vacancies")
    created_at = models.DateTimeField(auto_now_add=True)
    recruiter = models.ForeignKey('job.Recruiter', on_delete=models.CASCADE, related_name="posted_jobs")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
