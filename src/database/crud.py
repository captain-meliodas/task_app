import logging
from src.database.connection import DbCrud
from src.models.schemas import Tasks
from pymongo.database import Database
from src.config.config import Settings
from src.models.custom_validation import PyObjectId

settings = Settings().get_settings()

class MongoCrud(DbCrud):
    """This class implements the business logic to perform CRUD operations in the Mongo DB"""

    def create_task(self,db: Database,payload: Tasks):
        """Create the task from the given payload"""

        return db.tasks.insert_one(payload.dict())

    def get_task_by_id(self,db: Database,_id: str):
        """Get the task by id"""

        task = db.tasks.find_one({"_id":PyObjectId(_id)})
        return Tasks.parse_obj(task) if task else None
    
    def get_tasks(self,db: Database, skip:int=0, limit: int=100):
        """method to get tasks with paginated response"""

        tasks = []
        index = 0
        print(db)

        for task in db.tasks.find():
            tasks.append(Tasks.parse_obj(task)) if index >= skip and len(tasks) < limit else None
            index += 1
        return tasks
    
    def update_task(self,db: Database,_id,updated_payload: Tasks):
        """method to update the task details"""
        filter = {"_id":PyObjectId(_id)}
        data = db.tasks.update_one(filter,{"$set": updated_payload.dict(exclude_none=True)})
        logging.info(f"Task: ${updated_payload.id} updated successfully")
        return data

    def remove(self,db: Database,_id: str):
        """method to delete the task details"""

        mongo_obj = db.tasks.delete_one({"_id":PyObjectId(_id)})
        return mongo_obj.deleted_count