from typing import Optional
from pydantic import BaseModel, Field

from .helper import PyObjectId, ObjectId


class User(BaseModel):
    __collection__: str = 'users'
    id: Optional[PyObjectId] = Field(alias='_id')
    email: str
    password: str
    salt: Optional[str]
    name: Optional[str]

    class Config:
        allow_population_by_field_name = True


class ResponseUser(BaseModel):
    id: Optional[PyObjectId]
    email: str = ...
    name: Optional[str]

    class Config:
        json_encoders = {
            ObjectId: lambda v: str(v), #TODO why does init() set id an ObjectId, not PyObjectId?
        }