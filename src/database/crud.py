from src.database.connection import DbCrud
from src.models.schemas import Tasks
from pymongo.database import Database
from src.models.custom_validation import PyObjectId

class MongoCrud(DbCrud):
    """This class implements the business logic to perform CRUD operations in the Mongo DB"""

    def create_task(self,db: Database,payload: Tasks):
        pass

    def get_task_by_id(self,db: Database,id: PyObjectId):
        pass
    
    def get_tasks(self,db: Database):
        pass
    
    def update_task(self,db: Database,updated_payload: Tasks):
        pass

    def remove(self,db: Database,id: PyObjectId):
        pass