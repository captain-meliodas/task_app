#!/usr/bin/python3
# coding= utf-8
from fastapi import APIRouter
from src.models.schemas import Tasks

router = APIRouter(
    prefix="/tasks",
    tags=["Task CRUDs"],
    responses={404: {"description": "Not found"}},
)

@router.get("",response_model=Tasks)
async def getAllTasks():
    """Route to return all the tasks from db"""

    #write business logic for fetching all tasks from db

    task = {
        "_id":"507f1f77bcf86cd799439011",
            "title":"adsasd",
            "userId":"adsasdqwdas",
            "status":"Todo",
            "contributors":[]
    }
    return task
