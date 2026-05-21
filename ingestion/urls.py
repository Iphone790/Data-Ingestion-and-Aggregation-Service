from django.urls import path

from .views import (
    EventCreateAPIView,
    BulkEventCreateAPIView,
    EventListAPIView,
    MetricsAPIView,
    HealthAPIView,
    ReadyAPIView,
)


urlpatterns = [

    path(
        "events",
        EventCreateAPIView.as_view(),
    ),

    path(
        "events/list",
        EventListAPIView.as_view(),
    ),

    path(
        "events/bulk",
        BulkEventCreateAPIView.as_view(),
    ),

    path(
        "metrics",
        MetricsAPIView.as_view(),
    ),

    path(
        "health",
        HealthAPIView.as_view(),
    ),

    path(
        "ready",
        ReadyAPIView.as_view(),
    ),
]