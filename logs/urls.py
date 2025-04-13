from django.urls import path

from logs.views import (
    ActionLogListView,
    NotificationCreateView,
    NotificationListView
)

urlpatterns = [
    path('api/logs/', ActionLogListView.as_view(), name='get_logs'),
    path('api/notifications/', NotificationListView.as_view(), name='get_notifications'),
    path('api/notifications/create/', NotificationCreateView.as_view(), name='create_notification'),
]
