import json

events = []

for i in range(5001):
    events.append({
        "event_id": str(i),
        "tenant_id": "tenant1",
        "source": "web",
        "event_type": "click",
        "timestamp": "2026-05-21T10:00:00Z",
        "payload": {}
    })

data = {
    "events": events
}

with open("bulk.json", "w") as f:
    json.dump(data, f)

print("bulk.json created")