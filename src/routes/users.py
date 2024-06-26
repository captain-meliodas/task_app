from fastapi import APIRouter, Depends, HTTPException, status, Security
from fastapi.security import (OAuth2PasswordBearer, SecurityScopes)
from fastapi.responses import JSONResponse
from src.database.connection import DbConnection
from src.database.crud import MongoUserCrud
from src.models.schemas import Users, TokenData, UserCreate, UsersResponse
from src.constants import ALL_SCOPES, DELETED_USER_MSG, USER_NOT_FOUND_MSG
from src.config.config import Settings
from jose import JWTError, jwt
from typing import List
from passlib.hash import sha256_crypt

settings = Settings.get_settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", scopes=ALL_SCOPES)
crud = MongoUserCrud()

users_router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users"],
    dependencies=[Depends(oauth2_scheme)],
    responses={
        404:  {
            "description": USER_NOT_FOUND_MSG
        }
    }
)

async def get_current_user(security_scopes: SecurityScopes, conn=Depends(DbConnection), token: str = Depends(oauth2_scheme)):
    """
    This function gets and validates user
    :param security_scopes: of type SecurityScopes that is list containing all scopes
    required by itself and all dependencies that use this as sub-dependency
    :param conn: dependency injection to share database connection
    :param token: OAuth2 compatible token
    """

    authenticate_value = f"Bearer scope='{security_scopes.scope_str}'" if security_scopes.scopes else "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, settings.hash_key,
                                algorithms=[settings.hash_algorithm])
        username: str = payload.get("sub")
        if not username:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except JWTError as error:
        raise credentials_exception from error
    
    user = crud.get_by_name(conn.db,username)
    if not user:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not enough permissions",
                    headers={"WWW-Authenticate": authenticate_value}
                )
    return user
    
    


async def get_current_active_user(current_user: Users = Depends(get_current_user)):
    """
    This function provides current user
    :param: current_user: security dependency on get_current_user
    """

    if not current_user.active:
        raise HTTPException(status_code=403, detail="The user is disabled")
    return current_user

@users_router.get("", response_model=List[UsersResponse])
async def getUser(conn=Depends(DbConnection), admin_user: Users = Security(get_current_active_user, scopes=["admin:user"])):
    """
    This function reads current user based on GET call
    :param current_user: dependency on get_current_active_user
    """
    users = crud.get_all(conn.db)
    return users

@users_router.get("/me", response_model=UsersResponse)
async def getUser(current_user: Users = Depends(get_current_active_user)):
    """
    This function reads current user based on GET call
    :param current_user: dependency on get_current_active_user
    """

    return current_user

def hash_password(password):
    """
    hash password method which encrypts the password using SHA256-Crypt password hash
    :param password: password
    """
    return sha256_crypt.hash(password)

@users_router.post("", response_model=UsersResponse)
async def create_user(user: UserCreate, conn=Depends(DbConnection), admin_user: Users = Security(get_current_active_user, scopes=["admin:user"])):
    """
    This function creates user based on POST call
    :param user: data class of user create type listing all the parameters required
    :param conn: dependency injection to share database connection
    """
    old_user = crud.get_by_name(conn.db, user.username)
    if old_user:
        raise HTTPException(
            status_code=400, detail="User already exists")

    user.hashed_password = hash_password(user.password)

    #set the create_by and create the new user
    user.created_by = admin_user.username
    new_user = crud.create(conn.db, user)
    if new_user.inserted_id:
        return crud.get_by_id(conn.db, str(new_user.inserted_id))

@users_router.delete("/delete/{username}", response_model=UsersResponse)
async def delete_user(username: str, conn=Depends(DbConnection), admin_user: Users = Security(get_current_active_user, scopes=["admin:user"])):
    """
    This function delete user based on POST call
    :param user: userId a type of ObjectId string
    :param conn: dependency injection to share database connection
    """
    old_user_deleted_count = crud.remove_by_name(conn.db, username)
    if old_user_deleted_count:
            return JSONResponse(status_code=200, content={
            "message": DELETED_USER_MSG.format(username)
        })

    raise HTTPException(
        status_code=404, detail=USER_NOT_FOUND_MSG)