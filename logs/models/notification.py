from django.db import models


class Notification(models.Model):
    user = models.ForeignKey(
        'authenticate.User', on_delete=models.CASCADE, related_name="notifications"
    )
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
