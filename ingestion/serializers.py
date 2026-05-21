from rest_framework import serializers
from .models import Event
from .validators import validate_utc_timestamp


class EventSerializer(serializers.ModelSerializer):

    timestamp = serializers.DateTimeField(
        validators=[validate_utc_timestamp]
    )

    class Meta:
        model = Event
        fields = "__all__"
        read_only_fields = ["created_at"]


class BulkEventSerializer(serializers.Serializer):

    events = EventSerializer(many=True)

    def validate_events(self, value):

        if len(value) > 5000:

            raise serializers.ValidationError(
                "Maximum 5000 events allowed"
            )

        return value