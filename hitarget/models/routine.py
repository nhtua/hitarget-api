from typing import Optional, List
from datetime import date, datetime
from pydantic import BaseModel, validator, Field

from .helper import PyObjectId, jsonify_fields
from hitarget.core.config import settings


class Checkpoint(BaseModel):
    date: date
    percentage: float = 0
    gain: int = Field(
        description='seconds user has gained on a daily routine',
        ge=0,
        le=settings.ROUTINE_MAX_SECONDS)
    is_running: bool = Field(
        description='Indicate a checkpoint is running or stopped',
        default=False)
    last_update: datetime = Field(
        description="Last time server received update from client")

    class Config:
        json_encoders = jsonify_fields(['date'])

    def to_mongo(self):
        data = self.dict()
        data['date'] = self.date.strftime("%Y-%m-%d")
        return data


class CheckpointInRequest(BaseModel):
    routine_id: str
    is_running: bool


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
        json_encoders = jsonify_fields(['date'])

    def to_mongo(self):
        if len(self.repeat):
            for i, v in enumerate(self.repeat):
                self.repeat[i] = v.to_mongo()
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
    repeat: List[Checkpoint] = []

    class Config:
        allow_population_by_field_name = True
        json_encoders = jsonify_fields(['ObjectId', 'date'])


class RoutineInResponse(Routine):
    id: Optional[PyObjectId]
    repeat: List[Checkpoint] = []

    class Config:
        json_encoders = jsonify_fields(['ObjectId', 'date', 'datetime'])


class FormAddRoutine(Routine):
    """Form to add routine"""
