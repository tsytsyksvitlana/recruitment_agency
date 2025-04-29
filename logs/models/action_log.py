from django.db import models


class ActionLog(models.Model):
    user = models.ForeignKey(
        'authenticate.User', on_delete=models.SET_NULL, null=True, related_name="action_logs"
    )
    action = models.TextField()
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
