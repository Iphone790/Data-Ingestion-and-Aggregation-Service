import pytest
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


client = APIClient()


def test_idempotent_event_ingestion():

    payload = {
        "event_id": "abc123",
        "tenant_id": "tenant1",
        "source": "web",
        "event_type": "click",
        "timestamp": "2026",
    }