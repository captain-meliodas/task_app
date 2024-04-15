from fastapi import APIRouter, Depends, HTTPException, status
from src.database.connection import DbConnection
from src.config.config import Settings
from src.database.crud import MongoUserCrud
from passlib.hash import sha256_crypt
from jose import jwt
from fastapi.security import (OAuth2PasswordRequestForm)
from src.constants import USER_NOT_FOUND_MSG


settings = Settings.get_settings()
crud = MongoUserCrud()

token_router = APIRouter(
    prefix="/api/v1/token",
    tags=["Token"],
    responses={
        404:  {
            "description": USER_NOT_FOUND_MSG
        }
    })

def verify_password(plain_password: str, hashed_password: str):
    """
    verify password compares plain_password with hashed password
    :param plain_password: plain password of type string
    :param hashed_password: hashed password of type string
    """
    return sha256_crypt.verify(plain_password, hashed_password)

def authenticate_user(db, username: str, password: str, scopes: list):
    """
    This function authenticates user based on username and password
    :param db: refers to current database object
    :param username: username of type string
    :param password: password of type string
    :param scopes: list of user permissions
    """
    user = crud.get_by_name(db, username)
    if not (user and verify_password(password, user.hashed_password)):
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")
    for scope in scopes:
        if scope not in user.scopes:
            raise HTTPException(status_code=401, detail="Unauthorized")

    return user

def create_access_token(data: dict):
    """
    This function creates access token by encoding a claims set and returns a JWT string.
    :param data: data of type dict
    """
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, settings.hash_key,
                             algorithm=settings.hash_algorithm)
    return encoded_jwt

@token_router.post("")
async def login_for_access_token(conn=Depends(DbConnection),
                                 form_data: OAuth2PasswordRequestForm = Depends()):
    """
    This function authenticates the user and returns access token
    :param conn: dependency injection to share database connection
    :param form_data: OAuth2 compatible token login, get an access token for future requests
    """
    user = authenticate_user(conn.db, form_data.username, form_data.password, form_data.scopes)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.username, "scopes": form_data.scopes})
    return {"access_token": access_token, "token_type": "bearer"}
