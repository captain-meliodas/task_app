import logging
from src.database.connection import DbCrud
from src.models.schemas import Tasks, Users,UsersResponse
from pymongo.database import Database
from src.config.config import Settings
from src.models.custom_validation import PyObjectId

settings = Settings().get_settings()

class MongoTaskCrud(DbCrud):
    """This class implements the business logic to perform CRUD operations for task in the Mongo DB"""

    def create(self,db: Database,payload: Tasks):
        """Create the task from the given payload"""

        return db.tasks.insert_one(payload.dict())

    def get_by_id(self,db: Database,_id: str):
        """Get the task by id"""

        task = db.tasks.find_one({"_id":PyObjectId(_id)})
        return Tasks.parse_obj(task) if task else None
    
    def get_all(self,db: Database, tasks_filters, skip:int=0, limit: int=100):
        """method to get tasks with paginated response"""

        tasks = []
        index = 0

        for task in db.tasks.find(tasks_filters):
            tasks.append(Tasks.parse_obj(task)) if index >= skip and len(tasks) < limit else None
            index += 1
        return tasks
    
    def update_by_id(self,db: Database,_id,updated_payload: Tasks):
        """method to update the task details"""
        filter = {"_id":PyObjectId(_id)}
        task_obj = db.tasks.update_one(filter,{"$set": updated_payload.dict(exclude_none=True)})
        logging.info(f"Task: ${updated_payload.id} updated successfully")
        return task_obj

    def remove_by_id(self,db: Database,_id: str):
        """method to delete the task details"""

        task_obj = db.tasks.delete_one({"_id":PyObjectId(_id)})
        return task_obj.deleted_count

class MongoUserCrud(DbCrud):
    """This class implements the business logic to perform CRUD operations for users in the Mongo DB"""

    def create(self,db: Database,payload: Users):
        """Create the user from the given payload"""

        return db.users.insert_one(payload.dict())

    def get_by_id(self,db: Database,_id: str):
        """Get the user by id"""

        user = db.users.find_one({"_id":PyObjectId(_id)})
        return Users.parse_obj(user) if user else None

    def get_by_name(self,db: Database, username):
        user = db.users.find_one({"username":username})
        return Users.parse_obj(user) if user else None
    
    def get_all(self,db: Database, skip:int=0, limit: int=100):
        """method to get users with paginated response"""

        users = []
        index = 0

        for user in db.users.find():
            users.append(Users.parse_obj(user)) if index >= skip and len(user) < limit else None
            index += 1
        return users
    
    def update_by_id(self,db: Database,_id,updated_payload: Tasks):
        """method to update the user details"""
        filter = {"_id":PyObjectId(_id)}
        user_obj = db.users.update_one(filter,{"$set": updated_payload.dict(exclude_none=True)})
        logging.info(f"User: ${updated_payload.id} updated successfully")
        return user_obj

    def remove_by_name(self,db: Database,username: str):
        """method to delete the user details"""

        user_obj = db.users.delete_one({"username":username})
        return user_obj.deleted_count