from typing import Optional, List, Any
from datetime import datetime, date
from sqlmodel import Field, SQLModel, Column
from sqlalchemy import JSON
from enum import Enum


class StatusType(str, Enum):
    ANWESEND = "ANWESEND"
    URLAUB = "URLAUB"
    BILDUNGSURLAUB = "BILDUNGSURLAUB"
    KONGRESS = "KONGRESS"
    SONSTIGES = "SONSTIGES"


class Status(SQLModel, table=True):
    """Current status of the laboratory"""
    id: Optional[int] = Field(default=None, primary_key=True)
    type: StatusType = Field(default=StatusType.ANWESEND)
    date_from: Optional[date] = None
    date_to: Optional[date] = None
    description: Optional[str] = None
    next_return: Optional[date] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class StandardHours(SQLModel, table=True):
    """Standard weekly opening hours"""
    id: Optional[int] = Field(default=None, primary_key=True)
    day_of_week: int = Field(ge=0, le=6)  # 0=Monday, 6=Sunday
    time_ranges: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class HourException(SQLModel, table=True):
    """Exceptions to standard hours (holidays, special days)"""
    id: Optional[int] = Field(default=None, primary_key=True)
    exception_date: date = Field(index=True)
    closed: bool = Field(default=False)
    time_ranges: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    note: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Availability(SQLModel, table=True):
    """Indicative availability slots"""
    id: Optional[int] = Field(default=None, primary_key=True)
    availability_date: date = Field(index=True)
    time_slots: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Announcement(SQLModel, table=True):
    """News and announcements"""
    id: Optional[int] = Field(default=None, primary_key=True)
    lang: str = Field(default="de", index=True)
    title: str
    body: str
    active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Settings(SQLModel, table=True):
    """General settings stored as key-value pairs"""
    key: str = Field(primary_key=True)
    value: dict = Field(default_factory=dict, sa_column=Column(JSON))
    updated_at: datetime = Field(default_factory=datetime.utcnow)