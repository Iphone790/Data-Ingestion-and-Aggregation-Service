import pytest
from concurrent.futures import ThreadPoolExecutor
from rest_framework.test import APIClient
from ingestion.models import Event
from django.db import OperationalError

pytestmark = pytest.mark.django_db


def send_request():

    client = APIClient()

    payload = {
        "event_id": "concurrent_001",
        "tenant_id": "tenant1",
        "source": "web",
        "event_type": "click",
        "timestamp": "2026-05-21T10:00:00Z",
        "payload": {}
    }

    try:

        client.post(
            "/api/events",
            payload,
            format="json"
        )

    except OperationalError:
        pass


def test_concurrent_requests():

    with ThreadPoolExecutor(max_workers=2) as executor:

        futures = [
            executor.submit(send_request)
            for _ in range(2)
        ]

        for future in futures:
            future.result()

    count = Event.objects.filter(
        event_id="concurrent_001"
    ).count()

    assert count <= 1