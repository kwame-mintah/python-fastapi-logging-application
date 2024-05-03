import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@pytest.mark.parametrize(
    "size, expected_status_code, expected_len",
    [
        (10, status.HTTP_200_OK, 10),
        (1000, status.HTTP_200_OK, 1000),
    ],
)
def test_get_event_logs_returns_expected_size(
    size, expected_status_code, expected_len
) -> None:
    response = client.get(f"/v1/events/all?size={size}")
    assert response.status_code == expected_status_code
    assert len(response.json()) == expected_len


def test_get_event_logs_will_not_return_over_1000() -> None:
    response = client.get("/v1/events/all?size=1001")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "detail": [
            "Input should be less than or equal to 1000 found in ('query', 'size')"
        ]
    }


def test_get_single_event_log() -> None:
    response = client.get("/v1/events/get/u_123")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "type": "user",
        "timestamp": "2024-01-01T13:45:00Z",
        "event_id": "u_123",
        "event": {
            "username": "my_user",
            "email": "my_user@email.com",
            "operation": "read/write",
        },
    }


def test_get_single_event_log_not_found() -> None:
    response = client.get("/v1/events/get/u_404")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Unable to find event log with u_404"}


def test_insert_event_logs_valid_event() -> None:
    body = [
        {
            "type": "system",
            "timestamp": "2006-01-13T00:00:00Z",
            "event_id": "s_123",
            "event": {"system_id": "id_123", "location": "europe", "operation": "read"},
        }
    ]
    response = client.post(url="/v1/events/insert", json=body)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == [{"event_id": "s_123", "success": True, "error": ""}]


def test_insert_event_logs_invalid_event() -> None:
    body = [
        {
            "type": "system",
            "timestamp": "2006-01-13T00:00:00Z",
            "event_id": "s_123",
            "event": {"system_id": "id_123", "location": "jetix", "operation": "read"},
        }
    ]
    response = client.post(url="/v1/events/insert", json=body)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == [
        {"event_id": "s_123", "success": False, "error": "invalid_location"}
    ]


def test_insert_event_logs_valid_and_invalid_events() -> None:
    body = [
        {
            "type": "user",
            "timestamp": "2006-01-13T00:00:00Z",
            "event_id": "u_123",
            "event": {
                "username": "my_user",
                "email": "my_user@email.com",
                "operation": "read/write",
            },
        },
        {
            "type": "system",
            "timestamp": "2006-01-13T00:00:00Z",
            "event_id": "s_123",
            "event": {"system_id": "id_123", "location": "jetix", "operation": "read"},
        },
    ]
    response = client.post(url="/v1/events/insert", json=body)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == [
        {"error": "", "event_id": "u_123", "success": True},
        {"error": "invalid_location", "event_id": "s_123", "success": False},
    ]
