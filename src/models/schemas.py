from enum import Enum
from pydantic import BaseModel, Field, validator
from src.models.custom_validation import PyObjectId
from typing import Optional, List

class AuthScopeEnum(str,Enum):
    TASK_READ="task:read"
    TASK_WRITE="task:write"
    TASK_DELETE="task:delete"

class Status(str, Enum):
    TODO = "Todo"
    IN_PROGRESS = "In Progress"
    DONE = "Done"

class User(BaseModel):
    username: str
    email: str
    active: bool = True
    scopes: List[AuthScopeEnum]

class Tasks(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    title: str
    userId: str
    status: Status = "Todo"
    contributors: Optional[List[str]]

    @validator('title')
    def validate_title(cls,title: str):
        if title:
            return title.strip()
        raise ValueError("Title value must be provided")
