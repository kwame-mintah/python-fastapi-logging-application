from typing import List, Annotated

from fastapi import APIRouter, Depends, status, Query, Body

from app.dependencies import get_demo_service
from app.models.event_models import (
    EventLog,
    InsertResult,
    EventsErrorMessage,
    SystemEvent,
)
from app.services.demo_service import DemoService

router = APIRouter(prefix="/v1/events", tags=["events"])


@router.get(
    path="/all",
    operation_id="allEvents",
    summary="Retrieve all system and user log event types",
    response_model=List[EventLog],
    responses={400: {"model": EventsErrorMessage}, 500: {"model": EventsErrorMessage}},
    status_code=status.HTTP_200_OK,
)
async def get_event_logs(
    size: Annotated[int, Query(gt=0, le=1000)] = 10,
    service: DemoService = Depends(get_demo_service()),
) -> List[EventLog]:
    """
    Return a number of stored event logs. Maximum of 1000 events are returned.

    :param size: number of log events to return.
    :param service: service layer for queries.
    :return: list of event logs.
    """
    return service.return_event_logs(size)


@router.get(
    path="/get/{event_id}",
    operation_id="getEvent",
    summary="Retrieve a single log event",
    response_model=EventLog,
    responses={404: {"model": EventsErrorMessage}, 500: {"model": EventsErrorMessage}},
    status_code=status.HTTP_200_OK,
)
async def get_event_log(
    event_id: str,
    service: DemoService = Depends(get_demo_service()),
) -> EventLog:
    """
    Retrieve log event based on the event ID.

    :param event_id: event log to return.
    :param service: service layer for queries.
    :return: single event log.
    """
    return service.return_event_log(event_id=event_id)


@router.post(
    path="/insert",
    operation_id="insertEvents",
    summary="Insert user and/or system event log types",
    response_model=List[InsertResult],
    responses={400: {"model": EventsErrorMessage}, 500: {"model": EventsErrorMessage}},
    status_code=status.HTTP_201_CREATED,
)
async def insert_event_logs(
    event: List[
        Annotated[
            dict,
            Body(
                default=EventLog(
                    type="system",
                    timestamp="2006-01-13T00:00:00.000Z",
                    event_id="s_123",
                    event=SystemEvent(
                        system_id="id_123", location="europe", operation="read"
                    ),
                ).model_dump()
            ),
        ]
    ],
    service: DemoService = Depends(get_demo_service()),
) -> List[InsertResult]:
    """
    Insert new event logs. Maximum of 1000 can be inserted in a single request.

    :param event: list of event logs.
    :param service: service layer for queries.
    :return: list containing outcomes.
    """
    return service.insert_event_logs(event)
