from enum import Enum
from pydantic import BaseModel, Field, validator
from src.models.custom_validation import PyObjectId
import re
from typing import Optional, List

class AuthScopeEnum(str,Enum):
    TASK_READ="task:read"
    TASK_WRITE="task:write"
    TASK_DELETE="task:delete"
    ADMIN_USER="admin:user"

class Status(str, Enum):
    TODO = "Todo"
    IN_PROGRESS = "In Progress"
    DONE = "Done"

class TokenData(BaseModel):
    """ This class defines token data """
    username: Optional[str] = None
    scopes: List[str] = []

class Users(BaseModel):
    username: str
    email: str
    active: bool = True
    scopes: List[AuthScopeEnum]
    created_by: Optional[str]
    hashed_password: Optional[str]

class UserCreate(Users):
    password: str

    @validator('password')
    def validate_password(cls, password):
        pattern = re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d@$!%*?&]{16,}$")
        if not pattern.fullmatch(password):
            raise ValueError(
                f"password should contain minimum 16 characters, one uppercase, one lowercase and one number")
        return password

class UsersResponse(BaseModel):
    username: str
    email: str
    active: bool = True
    scopes: List[AuthScopeEnum]
    created_by: str



class Tasks(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    title: str
    userId: Optional[str]
    status: Status = "Todo"
    contributors: Optional[List[str]]

    @validator('title')
    def validate_title(cls,title: str):
        stripped_title = title.strip()
        if stripped_title:
            return stripped_title
        raise ValueError("Title value must be provided")
