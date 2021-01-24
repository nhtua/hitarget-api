from typing import Optional, List
from pydantic import BaseModel, validator, Field
from datetime import date, datetime

from .helper import PyObjectId, ObjectId
from hitarget.core.config import settings


class RepeatCheckpoint(BaseModel):
    date: date
    percentage: int = 0
    gain: int = Field(
        description='seconds user has gained on a daily routine',
        gt=0,
        lt=settings.ROUTINE_MAX_SECONDS
    )


class Routine(BaseModel):
    __collection__: str = 'routines'
    summary: str        = Field(
        description="Summary of daily routine",
        min_length=3,
        max_length=92
    )
    note: Optional[str] = Field(
        description="long note for the details of this routine",
        min_length=0,
        max_length=500
    )
    duration: int       = Field(
        description="duration in seconds each day.",
        gt=0,
        lt=settings.ROUTINE_MAX_SECONDS
    )
    end_date: Optional[date] = Field(
        description="this routine will end at the date",
    )
    repeat: List[RepeatCheckpoint] = []

    @validator('end_date')
    def min_end_date(cls, v):
        if v <= date.today():
            raise ValueError('End date must be in future')
        return v


class RoutineInDB(Routine):
    id: Optional[PyObjectId] = Field(alias="_id")
    user_id: PyObjectId = Field(...)
    created_at: datetime = Field(...)

    class Config:
        allow_population_by_field_name = True


class RoutineInResponse(Routine):
    id: Optional[PyObjectId]

    class Config:
        json_encoders = {
            ObjectId: lambda v: str(v),
        }


class FormAddRoutine(Routine):
    """Form to add routine"""
