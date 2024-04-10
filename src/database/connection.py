
from abc import ABC
class DbCrud(ABC):
    """ This is the abstract class who defines the crud methods needs to be implemented for Mongo CRUDs"""
    
    def create(self,db,payload):
        pass

    def get_by_id(self,db,id):
        pass
    
    def get_all(self,db):
        pass
    
    def update(self,db,updated_payload):
        pass

    def remove(self,db,id):
        pass

class DbConnection:
    """Dependency class for providing the db connection to fastApi routes"""
    
    def __init__(self):
        from src.database.mongo import MongoDB
        self.db = MongoDB.get_db_cursor()

    