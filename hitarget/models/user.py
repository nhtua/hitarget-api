from typing import Optional
from pydantic import BaseModel, Field

from .helper import PyObjectId, ObjectId
from hitarget.core import security


class User(BaseModel):
    __collection__: str = 'users'
    email: str
    name: Optional[str]

    def to_mongo(self):
        data = self.dict()
        data.pop('id', None)
        return data


class UserInResponse(User):
    id: Optional[PyObjectId]
    token: Optional[str]

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

    def check_password(self, password: str) -> bool:
        return security.verify_password(self.salt + password, self.password)

    def change_password(self, password: str) -> None:
        self.salt = security.generate_salt()
        self.password = security.get_password_hash(self.salt + password)


class FormLogin(BaseModel):
    email: str = Field(...)
    password: str = Field(...)


class FormRegister(BaseModel):
    email: str = Field(...)
    password: str = Field(...)
    name: Optional[str]
