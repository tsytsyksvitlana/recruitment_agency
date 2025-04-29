from django.db.models.signals import post_save
from django.dispatch import receiver

from logs.models.action_log import ActionLog
from logs.models.notification import Notification


@receiver(post_save, sender=ActionLog)
def create_notification_from_action_log(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.user,
            message=instance.action
        )
