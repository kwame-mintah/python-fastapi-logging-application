from fastapi import HTTPException
from typing import List

from app.models.event_models import EventLog


class DemoService:
    """
    Provide mock response to represent expected API response(s).
    """

    def return_event_logs(self, size: int) -> List[EventLog]:
        """
        Create a number of event logs depending on the size
        provided.

        **NOTE**:
        """
        return self.example_stub_data(size=size)

    def return_event_log(self, event_id: str) -> EventLog:
        """
        Get a single event log using the `event_id`
        """
        return self.example_event_stub_data(event_id)

    @staticmethod
    def example_stub_data(size: int) -> List[EventLog]:
        """
        Loop through and create a number of event logs
        and return a list of `EventLogs`.
        """
        example_list = []
        for i in range(size):
            event = EventLog(
                **dict(
                    {
                        "type": "system",
                        "timestamp": "2024-01-01T13:45:00.000Z",
                        "event_id": f"s_{i:03}",
                        "event": {
                            "system_id": f"id_1{i:02}",
                            "location": "europe",
                            "operation": "read/write",
                        },
                    }
                )
            )
            example_list.append(event)
        return example_list

    @staticmethod
    def example_event_stub_data(event_id: str):
        """
        Provide a single user event log. Any attempts to retrieve
        another `event_id` will return a 404 HTTP error.
        """
        user_event = EventLog(
            **dict(
                {
                    "type": "user",
                    "timestamp": "2024-01-01T13:45:00.000Z",
                    "event_id": "u_123",
                    "event": {
                        "username": "my_user",
                        "email": "my_user@email.com",
                        "operation": "read/write",
                    },
                }
            )
        )
        if event_id != user_event.event_id:
            raise HTTPException(
                status_code=404, detail=f"Unable to find event log with {event_id}"
            )
        return user_event
