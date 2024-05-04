import pytest
from fastapi import HTTPException, status

from app.models.event_models import EventLog, UserEvent, InsertResult
from app.services import demo_service
from app.services.demo_service import DemoService


def test_should_return_event_logs() -> None:
    service = DemoService()
    result = service.return_event_logs(size=1)
    assert len(result) == 1


def test_return_event_logs_raises_http_500_exception(monkeypatch) -> None:
    monkeypatch.setattr(demo_service, "PICKLE_FILENAME", "invalid")
    with pytest.raises(HTTPException) as e:
        demo_service.DemoService().example_return_event_logs(size=1)
    assert e.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


def test_should_return_single_event_log() -> None:
    service = DemoService()
    result = service.return_event_log(event_id="u_001")
    assert result == EventLog(
        type="user",
        timestamp="2024-01-01T13:45:10Z",
        event_id="u_001",
        event=UserEvent(
            username="my_user", email="my_user@email.com", operation="read"
        ),
    )


def test_return_event_log_raises_http_500_exception(monkeypatch) -> None:
    monkeypatch.setattr(demo_service, "PICKLE_FILENAME", "invalid")
    with pytest.raises(HTTPException) as e:
        demo_service.DemoService().example_return_event_log(event_id="u_001")
    assert e.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


def test_return_event_log_raises_http_404_exception() -> None:
    with pytest.raises(HTTPException) as e:
        demo_service.DemoService().example_return_event_log(event_id="u_007")
    assert e.value.status_code == status.HTTP_404_NOT_FOUND


def test_should_insert_valid_event_log() -> None:
    service = DemoService()
    example_event_log = [
        {
            "type": "system",
            "timestamp": "2006-01-13T00:00:00Z",
            "event_id": "s_123",
            "event": {"system_id": "id_123", "location": "europe", "operation": "read"},
        }
    ]
    result = service.insert_event_logs(event_logs=example_event_log)
    assert result == [InsertResult(event_id="s_123", success=True, error="")]


def test_should_not_insert_invalid_event_log() -> None:
    service = DemoService()
    example_event_log = [
        {
            "type": "system",
            "timestamp": "2006-01-13T00:00:00Z",
            "event_id": "s_123",
            "event": {"system_id": "id_123", "location": "jetix", "operation": "read"},
        }
    ]
    result = service.insert_event_logs(event_logs=example_event_log)
    assert result == [
        InsertResult(event_id="s_123", success=False, error="invalid_location")
    ]


def test_insert_event_logs_raises_http_400_exception(monkeypatch) -> None:
    example_event_log = [
        {
            "type": "system",
            "timestamp": "2006-01-13T00:00:00Z",
            "event_id": "s_123",
            "event": {"system_id": "id_123", "location": "jetix", "operation": "read"},
        },
        {
            "type": "user",
            "timestamp": "2023-10-01T13:45:00.000Z",
            "event_id": "u_123",
            "event": {
                "username": "my_user",
                "email": "my_user@email.com",
                "operation": "write",
            },
        },
    ]
    monkeypatch.setattr(demo_service, "MAX_SIZE", 1)
    with pytest.raises(HTTPException) as e:
        demo_service.DemoService().insert_event_logs(event_logs=example_event_log)
    assert e.value.status_code == status.HTTP_400_BAD_REQUEST
