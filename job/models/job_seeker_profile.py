from django.db import models


class JobSeekerProfile(models.Model):
    user = models.OneToOneField(
        'job.JobSeeker',
        on_delete=models.CASCADE,
        related_name="profile",
        db_index=True
    )
    skills = models.TextField(blank=True)
    experience = models.TextField(blank=True)
    education = models.TextField(blank=True)
    location = models.ForeignKey(
        'job.Location',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="jobseekers",
        db_index=True
    )

    def __str__(self):
        return f"Profile of {self.user.user.email}"
