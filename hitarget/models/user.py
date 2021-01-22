from typing import Optional
from pydantic import BaseModel, Field

from .helper import PyObjectId, ObjectId


class User(BaseModel):
    __collection__: str = 'users'
    email: str
    name: Optional[str]


class UserInResponse(User):
    id: Optional[PyObjectId]

    class Config:
        json_encoders = {
            # The workaround's https://github.com/tiangolo/fastapi/issues/1515
            ObjectId: lambda v: str(v),
        }


class UserInDB(User):
    id: Optional[PyObjectId] = Field(alias='_id')
    password: str
    salt: Optional[str]

    class Config:
        allow_population_by_field_name = True
