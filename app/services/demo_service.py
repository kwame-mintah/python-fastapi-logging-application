from typing import List, Any

from fastapi import HTTPException
from pydantic import ValidationError
import pickle

from app.models.event_models import EventLog, InsertResult

MAX_SIZE = 1000
PICKLE_FILENAME = "data/logging.pkl"


class DemoService:
    """
    Provide mock response to represent expected API response(s).
    """

    def return_event_logs(self, size: int) -> List[EventLog]:
        """
        Return event logs stored within archive.
        """
        return self.example_stub_data(size=size)

    def return_event_log(self, event_id: str) -> EventLog:
        """
        Return a single event log using the `event_id`.
        """
        return self.example_event_stub_data(event_id)

    def insert_event_logs(self, event_logs: List[dict]) -> List[InsertResult]:
        """
        Insert event logs into archive.
        """
        if len(event_logs) > MAX_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"Unable to process event logs, must be less than {MAX_SIZE}. Received: {len(event_logs)}",
            )
        return self.example_insert_results(event_logs)

    @staticmethod
    def example_stub_data(size: int) -> List[EventLog]:
        """
        Load archive and return stored event logs. Returning set number
        using `size` provided.
        """
        try:
            with open(PICKLE_FILENAME, "r+b") as f:
                stored_events = pickle.load(f)[:size]
                return stored_events
        except IndexError:
            return []

    @staticmethod
    def example_event_stub_data(event_id: str):
        """
        Provide a single user event log stored within archive. If not found
        returns HTTPException 404 error.
        """
        try:
            with open(PICKLE_FILENAME, "r+b") as f:
                stored_events = pickle.load(f)
                result = list(
                    filter(lambda event: event.event_id == event_id, stored_events)
                )
                if not result:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Unable to find event log with {event_id}",
                    )
                return result[0]
        except (pickle.PicklingError, FileNotFoundError):
            raise HTTPException(
                status_code=500,
                detail=f"An error occurred when attempting to find event log with {event_id}",
            )

    @staticmethod
    def example_insert_results(events: List[dict]) -> List[InsertResult]:
        """
        Validate event logs received and return a list of results for each success
        or unsuccessful archive insertion(s).
        """
        results = []
        valid_events = []
        for event in events:
            try:
                event = EventLog(**event)
                valid_events.append(event)
                results.append(
                    InsertResult(event_id=event.event_id, success=True, error="")
                )
            except ValidationError as e:
                message = str(e)
                if "timestamp" in message:
                    message = "invalid_timestamp"
                elif "location" in message:
                    message = "invalid_location"

                results.append(
                    InsertResult(
                        event_id=event["event_id"] if event["event_id"] else "",
                        success=False,
                        error=message,
                    )
                )

        # TODO: Replace usage of `pickle` with a database.
        bulk_amend_existing_pickle_file(valid_events)
        return results


def bulk_amend_existing_pickle_file(contents: Any) -> None:
    """
    Open existing pickle file and load the data. Existing data
    should be a List of `EventLog`. Will write to existing pickle file
    using extended list (appending to the end).
    """
    previous_data = pickle.load(open(PICKLE_FILENAME, "rb"))
    previous_data.extend(contents)
    pickle.dump(previous_data, open(PICKLE_FILENAME, "wb"))
