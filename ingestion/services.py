from django.db import transaction, IntegrityError
from .models import Event


class EventService:

    @staticmethod
    def create_event(data):
        try:
            with transaction.atomic():
                event = Event.objects.create(**data)
                return event, True
        except IntegrityError:
            return None, False

    @staticmethod
    def bulk_create_events(events_data):
        objects = [Event(**event) for event in events_data]

        Event.objects.bulk_create(
            objects,
            ignore_conflicts=True,
            batch_size=1000,
        )