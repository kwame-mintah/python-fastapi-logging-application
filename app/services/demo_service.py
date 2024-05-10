import os
from typing import List, Any

from fastapi import HTTPException
from pydantic import ValidationError
import pickle

from app.models.event_models import EventLog, InsertResult

MAX_SIZE = 1000
PICKLE_FILENAME = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "data", "logging.pkl")
)


class DemoService:
    """
    Provide mock response to represent expected API response(s).
    """

    def return_event_logs(self, size: int) -> List[EventLog]:
        """
        Return event logs stored within archive.

        :param size: number of events to return
        :return: list of log events
        """
        return self.example_return_event_logs(size=size)

    def return_event_log(self, event_id: str) -> EventLog:
        """
        Return a single event log using the `event_id`.

        :param event_id: event log to return based on `event_id`
        :return: event log
        """
        return self.example_return_event_log(event_id)

    def insert_event_logs(self, event_logs: List[dict]) -> List[InsertResult]:
        """
        Insert event logs into archive.

        :param event_logs: list of event log(s)
        :return: outcome of insert(s)
        """
        if len(event_logs) > MAX_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"Unable to process event logs, must be less than {MAX_SIZE}. Received: {len(event_logs)}",
            )
        return self.example_insert_event_logs_results(event_logs)

    @staticmethod
    def example_return_event_logs(size: int) -> List[EventLog]:
        """
        Load archive and return stored event logs. Returning set number
        using `size` provided.

        :param size: items from the beginning through stop using `size`
        :return: list of event logs
        """
        try:
            with open(PICKLE_FILENAME, "r+b") as f:
                stored_events = pickle.load(f)[:size]
                return stored_events
        except (pickle.PicklingError, FileNotFoundError, IndexError) as e:
            raise HTTPException(
                status_code=500,
                detail=f"An error occurred when attempting to retrieve all log records with: {e}",
            )

    @staticmethod
    def example_return_event_log(event_id: str):
        """
        Provide a single user event log stored within archive. If not found
        returns HTTPException 404 error.

        :param event_id: event_id to use as a filter
        :return: event log
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
    def example_insert_event_logs_results(events: List[dict]) -> List[InsertResult]:
        """
        Validate event logs received and return a list of results for each success
        or unsuccessful archive insertion(s).

        :param events: list of dicts
        :return: outcome of insert(s)
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

    :param contents: list of event logs
    """
    previous_data = pickle.load(open(PICKLE_FILENAME, "rb"))
    previous_data.extend(contents)
    pickle.dump(previous_data, open(PICKLE_FILENAME, "wb"))
