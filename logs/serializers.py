from rest_framework import serializers

from logs.models.action_log import ActionLog
from logs.models.notification import Notification


class ActionLogSerializer(serializers.Serializer):
    class Meta:
        model = ActionLog
        fields = ['id', 'user', 'action', 'timestamp']


class NotificationSerializer(serializers.Serializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'message', 'created_at']
