#!/usr/bin/python3
# coding= utf-8
""" pydantic objectid """
from bson import ObjectId


class PyObjectId(ObjectId):
    """ This class defines and validates object id"""

    @classmethod
    def __get_validators__(cls):
        """ get validators """
        yield cls.validate

    @classmethod
    def validate(cls, var):
        """ This function validates and returns objectId as a string """
        if not ObjectId.is_valid(var):
            raise ValueError('Invalid objectid')
        return str(var)

    @classmethod
    def __modify_schema__(cls, field_schema):
        """ This method modify schema to return objectId as string"""
        field_schema.update(type='string')