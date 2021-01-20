from typing import Optional
from pydantic import BaseModel, Field

from .helper import PyObjectId


class User(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    email: str
    password: str
    salt: Optional[str]
    name: Optional[str]

    class Config:
        allow_population_by_field_name = True
