#!/usr/bin/python3
# coding= utf-8
from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.responses import JSONResponse
from typing import List
from src.models.schemas import Tasks, Users
from src.routes.users import get_current_active_user
from src.database.connection import DbConnection
from src.database.crud import MongoTaskCrud
from src.constants import TASK_NOT_FOUND_MSG, DELETED_TASK_MSG

task_router = APIRouter(
    prefix="/api/v1/tasks",
    tags=["Task CRUDs"],
    responses={404: {"description": "Not found"}},
)

crud = MongoTaskCrud()

@task_router.get("",response_model=List[Tasks])
async def getAllTasks(skip: int = 0, limit: int = 100, conn=Depends(DbConnection),current_user: Users = Security(get_current_active_user, scopes=["task:read"])):
    """Route to return all the tasks from db"""
    data = crud.get_all(conn.db,skip,limit)
    return data

@task_router.get("/{task_id}",response_model=Tasks)
async def getTask(task_id:str, conn=Depends(DbConnection), current_user: Users = Security(get_current_active_user, scopes=["task:read"])):
    """Route to return all the tasks from db"""

    data = crud.get_by_id(conn.db,task_id)
    if not data:
        raise HTTPException(status_code=404,detail=TASK_NOT_FOUND_MSG)
    
    return data

@task_router.post("",response_model=Tasks, status_code=201)
async def createTask(payload: Tasks, conn=Depends(DbConnection)):
    """Route to return all the tasks from db"""
    
    # create the task
    inserted_data = crud.create(conn.db,payload)

    if inserted_data.inserted_id:
        #fetch and return the created task
        data = crud.get_by_id(conn.db,inserted_data.inserted_id)
    else:
        raise HTTPException(status_code=404,detail=TASK_NOT_FOUND_MSG)
    
    return data

@task_router.put("/update/{task_id}",response_model=Tasks)
async def updateTask(task_id:str ,payload: Tasks, conn=Depends(DbConnection)):
    """Route to return all the tasks from db"""
    # update the task
    data = crud.update_by_id(conn.db,task_id,payload)
    if data.matched_count:
    #fetch and return the created task
        data = crud.get_by_id(conn.db,task_id)
    else:
        raise HTTPException(status_code=404,detail=TASK_NOT_FOUND_MSG)
    return data

@task_router.delete("/delete/{task_id}")
async def removeTask(task_id:str, conn=Depends(DbConnection)):
    """Route to return all the tasks from db"""
    # remove the task
    
    deleted_count = crud.remove_by_id(conn.db,task_id)
    if not deleted_count:
        raise HTTPException(status_code=404,detail=TASK_NOT_FOUND_MSG)
    
    return JSONResponse(status_code=200, content={
        "message": DELETED_TASK_MSG.format(task_id)
    })
