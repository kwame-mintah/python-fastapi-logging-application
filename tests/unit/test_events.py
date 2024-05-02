import pytest
from fastapi.testclient import TestClient
from fastapi import status

from app.main import app

client = TestClient(app)


@pytest.mark.parametrize(
    "size, expected_status_code, expected_len",
    [
        (10, status.HTTP_200_OK, 10),
        (999, status.HTTP_200_OK, 999),
    ],
)
def test_get_event_logs_returns_expected_size(size, expected_status_code, expected_len):
    response = client.get(f"/v1/events/all?size={size}")
    assert response.status_code == expected_status_code
    assert len(response.json()) == expected_len


def test_get_event_logs_will_not_return_over_1000():
    response = client.get("/v1/events/all?size=1000")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "detail": "Input should be less than 1000",
        "reason": {"size": "1000"},
    }


def test_get_single_event_log():
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


def test_get_single_event_log_not_found():
    response = client.get("/v1/events/get/u_404")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Unable to find event log with u_404"}
