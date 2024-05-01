from enum import Enum

from pydantic import BaseModel, PastDatetime, Field, EmailStr


class Locations(str, Enum):
    """
    System type events must be either "europe" or "us"
    """
    europe = 'europe'
    us = 'us'


class UserEvent(BaseModel):
    """
    The user event log received
    """
    username: str = Field(title="The username associated with the event", examples=["ben_tennyson"])
    email: EmailStr = Field(title="The email address associated to the user account", examples=["ben_tennyson@cartoonnetwork.com"])
    operation: str = Field(title="Operation carried out by the user", examples=["read", "write"])


class SystemEvent(BaseModel):
    """
    The system event log received
    """
    system_id: str = Field(title="System generated id associated with the log event")
    location: Locations = Field(title="Location where the system is based", examples=["us", "europe"])
    operation: str = Field(title="Operation carried out by the system", examples=["read", "write"])


class Event(BaseModel):
    """
    The event log received
    """
    type: str = Field(title="The type of event received", examples=["user", "system"])
    timestamp: PastDatetime = Field(title="Time event took place (must be in the past)")
    event_id: str = Field(title="Unique id for event received", examples=["u_123"])


class UserEventLog(Event):
    """
    Incoming or stored user event log
    """
    event: UserEvent


class SystemEventLog(Event):
    """
    Incoming or stored system event log
    """
    event: SystemEvent


class InsertResult(BaseModel):
    """
    Result outcome of inserting user and/or system events
    """
    event_id: str = Field(title="The event id provided", examples=["u_123", "s_125"])
    success: bool = Field(title="Result of insertion", examples=[True, False])
    error: str | None = Field(default=None, title="Reason for failed log insertion", examples=["invalid_timestamp", "invalid_location"])

