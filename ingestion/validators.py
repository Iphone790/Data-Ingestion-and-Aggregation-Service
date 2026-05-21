from django.utils.dateparse import parse_datetime
from rest_framework import serializers
from django.utils.timezone import (
    is_naive,
    make_aware,
)
import pytz


def validate_utc_timestamp(value):

    dt = parse_datetime(str(value))

    if not dt:

        raise serializers.ValidationError(
            "Invalid timestamp"
        )

    if is_naive(dt):

        dt = make_aware(
            dt,
            timezone=pytz.UTC
        )

    return dt.astimezone(pytz.UTC)