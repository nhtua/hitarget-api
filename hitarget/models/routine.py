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
        le=settings.ROUTINE_MAX_SECONDS
    )
    end_date: Optional[date] = Field(
        description="this routine will end at the date",
    )

    class Config:
        json_encoders = {
            date: lambda v: v.strftime("%Y-%m-%d"),
        }

    @validator('end_date')
    def min_end_date(cls, v):
        if v is None:
            return v
        if v <= date.today():
            raise ValueError('End date must be in future')
        return v

    def to_mongo(self):
        data = self.dict()
        data.pop('id', None)
        d = data['end_date']
        data['end_date'] = datetime(year=d.year, month=d.month, day=d.day,
                                    hour=0, minute=0, second=0) if d is not None else None
        return data


class RoutineInDB(Routine):
    id: Optional[PyObjectId] = Field(alias="_id")
    user_id: PyObjectId = Field(...)
    created_at: datetime = Field(...)
    repeat: List[RepeatCheckpoint] = []

    class Config:
        allow_population_by_field_name = True


class RoutineInResponse(Routine):
    id: Optional[PyObjectId]
    repeat: List[RepeatCheckpoint] = []

    class Config:
        json_encoders = {
            ObjectId: lambda v: str(v),
            date: lambda v: v.strftime("%Y-%m-%d")
        }


class FormAddRoutine(Routine):
    """Form to add routine"""
