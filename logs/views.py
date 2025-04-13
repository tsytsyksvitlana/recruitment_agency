from django.utils.dateparse import parse_datetime
from rest_framework import generics
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from logs.models.action_log import ActionLog
from logs.models.notification import Notification
from logs.serializers import ActionLogSerializer, NotificationSerializer


class ActionLogListView(generics.ListAPIView):
    serializer_class = ActionLogSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter("start", openapi.IN_QUERY, description="Start datetime", type=openapi.TYPE_STRING, format='date-time'),
            openapi.Parameter("end", openapi.IN_QUERY, description="End datetime", type=openapi.TYPE_STRING, format='date-time'),
        ]
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        queryset = ActionLog.objects.all()
        start = self.request.query_params.get("start")
        end = self.request.query_params.get("end")

        if start:
            start = parse_datetime(start)
        if end:
            end = parse_datetime(end)

        if start and end:
            queryset = queryset.filter(timestamp__range=(start, end))
        elif start:
            queryset = queryset.filter(timestamp__gte=start)
        elif end:
            queryset = queryset.filter(timestamp__lte=end)

        return queryset


class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter("start", openapi.IN_QUERY, description="Start datetime", type=openapi.TYPE_STRING, format='date-time'),
            openapi.Parameter("end", openapi.IN_QUERY, description="End datetime", type=openapi.TYPE_STRING, format='date-time'),
        ]
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Notification.objects.all()
        start = self.request.query_params.get("start")
        end = self.request.query_params.get("end")

        if start:
            start = parse_datetime(start)
        if end:
            end = parse_datetime(end)

        if start and end:
            queryset = queryset.filter(created_at__range=(start, end))
        elif start:
            queryset = queryset.filter(created_at__gte=start)
        elif end:
            queryset = queryset.filter(created_at__lte=end)

        return queryset


class NotificationCreateView(generics.CreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
