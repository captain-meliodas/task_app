
from abc import ABC, abstractmethod
class DbCrud(ABC):
    """ This is the abstract class who defines the crud methods needs to be implemented for Mongo CRUDs"""
    
    @abstractmethod
    def create(self,db,payload):
        """Create the task from the given payload"""
        pass
    
    @abstractmethod
    def get_by_id(self,db,_id):
        """Get the task by id"""
        pass
    
    @abstractmethod
    def get_all(self,db, skip=0, limit=100):
        """method to get tasks with paginated response"""
        pass
    
    @abstractmethod
    def update_by_id(self,db,updated_payload):
        """method to update the task details"""
        pass
    
    @abstractmethod
    def remove_by_id(self,db,_id):
        """method to delete the task details"""
        pass

class DbConnection:
    """Dependency class for providing the db connection to fastApi routes"""
    
    def __init__(self):
        from src.database.mongo import MongoDB
        self.db = MongoDB.get_db_cursor()

    