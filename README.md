# Event Ingestion and Aggregation Service

## Overview

This project is a backend event ingestion and aggregation system built using Django and Django REST Framework.

The service supports:

* Single event ingestion
* Bulk event ingestion
* Idempotent event processing
* Event querying with filters
* Aggregated metrics APIs
* Background task processing using Celery
* Rate limiting and abuse protection
* Health and readiness checks
* Automated testing using Pytest

---

# Tech Stack

* Python 3.11
* Django 5
* Django REST Framework
* SQLite
* Celery
* Redis
* Pytest

---

# Project Features

## 1. Event Ingestion

### POST `/api/events`

Accepts a single event payload.

Features:

* Idempotent event creation
* Duplicate prevention using unique `event_id`
* Timestamp validation
* UTC timestamp enforcement

---

## 2. Bulk Event Ingestion

### POST `/api/events/bulk`

Accepts up to 5000 events in a single request.

Features:

* Bulk insertion optimization
* Payload validation
* Background aggregation trigger
* Graceful validation handling

---

## 3. Event Query API

### GET `/api/events/list`

Supports:

* Mandatory `tenant_id`
* Filtering by:

  * source
  * event_type
  * from timestamp
  * to timestamp
* Pagination
* Stable sorting

---

## 4. Metrics Aggregation

### GET `/api/metrics`

Supports:

* Minute-level aggregation
* Hour-level aggregation
* Aggregation by:

  * source
  * event_type

Optimized using database aggregation queries instead of in-memory processing.

---

## 5. Health Checks

### GET `/api/health`

Basic liveness endpoint.

### GET `/api/ready`

Checks database connectivity and readiness.

---

# Concurrency and Idempotency

The application safely handles duplicate requests using:

* Unique database constraints
* Transaction-safe event creation logic

This ensures:

* No duplicate event insertion
* Concurrency-safe idempotency

---

# Asynchronous Processing

Celery + Redis are used for background aggregation processing.

Background task:

* `aggregate_events_task`

This demonstrates:

* Non-blocking processing
* Asynchronous task execution
* Incremental aggregation

---

# Performance Optimizations

Implemented optimizations:

* Indexed database fields
* Bulk database insertion
* Query filtering optimization
* Pagination
* Aggregation at database level
* Rate limiting

---

# Security and Abuse Controls

Implemented protections:

* Payload size validation
* Request throttling
* UTC timestamp sanitization
* Duplicate event prevention

---

# API Endpoints

| Method | Endpoint           | Description              |
| ------ | ------------------ | ------------------------ |
| POST   | `/api/events`      | Create single event      |
| POST   | `/api/events/bulk` | Bulk event ingestion     |
| GET    | `/api/events/list` | List events with filters |
| GET    | `/api/metrics`     | Aggregated metrics       |
| GET    | `/api/health`      | Health check             |
| GET    | `/api/ready`       | Readiness check          |

---

# Local Setup

## 1. Clone Repository

```bash
git clone https://github.com/Iphone790/Data-Ingestion-and-Aggregation-Service.git

cd Data-Ingestion-and-Aggregation-Service
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

---

## 3. Activate Virtual Environment

### Linux / Mac

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

---

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 5. Run Database Migrations

```bash
python manage.py migrate
```

---

## 6. Start Redis Server

```bash
redis-server
```

---

## 7. Start Celery Worker

```bash
celery -A config worker --loglevel=info
```

---

## 8. Run Django Server

```bash
python manage.py runserver
```

---

# Running Tests

Run all tests:

```bash
pytest
```

---

# Example Event Payload

```json
{
  "event_id": "event_001",
  "tenant_id": "tenant_1",
  "source": "web",
  "event_type": "click",
  "timestamp": "2026-05-21T10:00:00Z",
  "payload": {
    "button": "signup"
  }
}
```

---

# Rate Limiting

DRF throttling is implemented to prevent abuse.

Example:

* `100 requests/minute`

---

# Docker Support

Project includes:

* Dockerfile
* docker-compose.yml

Run using Docker:

```bash
docker-compose up --build
```

---

# Automated Test Coverage

Pytest coverage includes:

* Idempotent event ingestion
* Bulk ingestion validation
* Aggregation correctness
* Concurrency safety
* Time window edge cases

---

# Author

Aditya Verma
