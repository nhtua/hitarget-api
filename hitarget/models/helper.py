from typing import List, Dict
from bson import ObjectId
from datetime import datetime, date


class PyObjectId(ObjectId):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')


class MongoDateObject():

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')


def jsonify_fields(fields: List[str], combined_with: Dict = {}):
    common = {}
    if "ObjectId" in fields:
        common[ObjectId] = lambda v: str(v)
    if "date" in fields:
        common[date] = lambda v: v.strftime("%Y-%m-%d")
    if "datetime" in fields:
        common[datetime] = lambda v: v.strftime("%Y-%m-%d %H:%M:%S")
    common.update(combined_with)
    return common
