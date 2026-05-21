from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Event, Aggregate
from .serializers import EventSerializer, BulkEventSerializer
from .services import EventService
from .tasks import aggregate_events_task
from .pagination import EventPagination
from .throttling import EventThrottle
from .tasks import aggregate_events_task


class EventCreateAPIView(APIView):

    throttle_classes = [EventThrottle]

    def post(self, request):

        serializer = EventSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        _, created = EventService.create_event(
            serializer.validated_data
        )

        if not created:

            return Response(
                {
                    "message":
                    "Duplicate event ignored"
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


class BulkEventCreateAPIView(APIView):

    throttle_classes = [EventThrottle]

    def post(self, request):

        serializer = BulkEventSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        EventService.bulk_create_events(
            serializer.validated_data["events"]
        )

        aggregate_events_task.delay()

        return Response(
            {"message": "Bulk events processed"},
            status=status.HTTP_201_CREATED,
        )

class EventListAPIView(APIView):

    def get(self, request):
        tenant_id = request.GET.get("tenant_id")

        if not tenant_id:
            return Response(
                {"error": "tenant_id is required"},
                status=400,
            )

        queryset = Event.objects.filter(tenant_id=tenant_id)

        source = request.GET.get("source")
        event_type = request.GET.get("event_type")
        start = request.GET.get("from")
        end = request.GET.get("to")

        if source:
            queryset = queryset.filter(source=source)

        if event_type:
            queryset = queryset.filter(event_type=event_type)

        if start:
            queryset = queryset.filter(timestamp__gte=start)

        if end:
            queryset = queryset.filter(timestamp__lte=end)

        queryset = queryset.order_by("timestamp")

        paginator = EventPagination()

        page = paginator.paginate_queryset(
            queryset,
            request
        )

        serializer = EventSerializer(
            page,
            many=True
        )

        return paginator.get_paginated_response(
            serializer.data
        )


class MetricsAPIView(APIView):
    throttle_classes = [EventThrottle]

    def get(self, request):
        tenant_id = request.GET.get("tenant_id")
        if not tenant_id:
            return Response(
                {"error": "tenant_id is required"},
                status=400,
            )

        queryset = Aggregate.objects.filter(
            tenant_id=tenant_id
        )

        bucket_size = request.GET.get("bucket_size")

        if bucket_size:
            queryset = queryset.filter(bucket_size=bucket_size)

        source = request.GET.get("source")
        event_type = request.GET.get("event_type")

        if source:
            queryset = queryset.filter(source=source)

        if event_type:
            queryset = queryset.filter(event_type=event_type)

        data = queryset.values(
            "bucket_start",
            "event_type",
            "source",
        ).annotate(total=Sum("count"))

        return Response(data)



class HealthAPIView(APIView):

    def get(self, request):
        return Response({"status": "ok"})


class ReadyAPIView(APIView):

    def get(self, request):
        try:
            Event.objects.exists()
            return Response({"database": "connected"})
        except Exception:
            return Response(
                {"database": "failed"},
                status=500,
            )