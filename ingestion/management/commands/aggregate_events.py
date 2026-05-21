from django.core.management.base import BaseCommand
from django.db.models import Count, Min, Max
from django.db.models.functions import TruncMinute, TruncHour

from ingestion.models import Event, Aggregate


class Command(BaseCommand):

    help = "Aggregate events"

    def handle(self, *args, **kwargs):

        Aggregate.objects.all().delete()

        # Minute aggregation
        minute_data = (
            Event.objects
            .annotate(
                bucket=TruncMinute("timestamp")
            )
            .values(
                "tenant_id",
                "source",
                "event_type",
                "bucket",
            )
            .annotate(
                total=Count("id"),
                first_seen=Min("timestamp"),
                last_seen=Max("timestamp"),
            )
        )

        for item in minute_data:

            Aggregate.objects.update_or_create(
                tenant_id=item["tenant_id"],
                bucket_start=item["bucket"],
                bucket_size="minute",
                source=item["source"],
                event_type=item["event_type"],

                defaults={
                    "count": item["total"],
                    "first_seen": item["first_seen"],
                    "last_seen": item["last_seen"],
                }
            )

        # Hour aggregation
        hour_data = (
            Event.objects
            .annotate(
                bucket=TruncHour("timestamp")
            )
            .values(
                "tenant_id",
                "source",
                "event_type",
                "bucket",
            )
            .annotate(
                total=Count("id"),
                first_seen=Min("timestamp"),
                last_seen=Max("timestamp"),
            )
        )

        for item in hour_data:

            Aggregate.objects.update_or_create(
                tenant_id=item["tenant_id"],
                bucket_start=item["bucket"],
                bucket_size="hour",
                source=item["source"],
                event_type=item["event_type"],

                defaults={
                    "count": item["total"],
                    "first_seen": item["first_seen"],
                    "last_seen": item["last_seen"],
                }
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Aggregation completed"
            )
        )