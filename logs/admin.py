from django.contrib import admin

from logs.models.action_log import ActionLog
from logs.models.notification import Notification


@admin.register(ActionLog)
class ActionLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'timestamp')
    list_filter = ('user', 'timestamp')
    search_fields = ('user__username', 'action')
    ordering = ('-timestamp',)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'message')
    ordering = ('-created_at',)
