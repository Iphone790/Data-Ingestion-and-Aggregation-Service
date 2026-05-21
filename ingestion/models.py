from django.db import models


class Event(models.Model):
    event_id = models.CharField(max_length=255, unique=True)
    tenant_id = models.CharField(max_length=255, db_index=True)
    source = models.CharField(max_length=100)
    event_type = models.CharField(max_length=100)
    timestamp = models.DateTimeField(db_index=True)
    payload = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["tenant_id", "timestamp"]),
            models.Index(fields=["source"]),
            models.Index(fields=["event_type"]),
        ]


class Aggregate(models.Model):
    BUCKET_CHOICES = [
        ("minute", "Minute"),
        ("hour", "Hour"),
    ]

    tenant_id = models.CharField(max_length=255)
    bucket_start = models.DateTimeField(db_index=True)
    bucket_size = models.CharField(max_length=20, choices=BUCKET_CHOICES)
    source = models.CharField(max_length=100, null=True, blank=True)
    event_type = models.CharField(max_length=100, null=True, blank=True)
    count = models.IntegerField(default=0)
    first_seen = models.DateTimeField()
    last_seen = models.DateTimeField()

    class Meta:
        indexes = [
            models.Index(
                fields=["tenant_id", "bucket_start"]
            ),
            models.Index(
                fields=["tenant_id", "event_type"]
            ),
            models.Index(
                fields=["tenant_id", "source"]
            ),
        ]

        unique_together = (
            "tenant_id",
            "bucket_start",
            "bucket_size",
            "source",
            "event_type",
        )