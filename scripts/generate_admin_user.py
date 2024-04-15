from src.database.connection import DbConnection
from src.database.crud import MongoUserCrud
from src.routes.users import hash_password
from src.models.schemas import UserCreate
from src.constants import ADMIN_USER_PASSWORD, ADMIN_USER_NAME

conn = DbConnection()
crud = MongoUserCrud()


def generate_admin_user(db=None,username=None,password=None):
    """method to create an admin user"""
    username = username if username else ADMIN_USER_NAME
    password = password if password else ADMIN_USER_PASSWORD
    user = UserCreate(username=username,email="email",scopes=[
            'task:read',
            'task:write',
            'task:delete',
            'admin:user'
        ],created_by="script", password=password)
    
    user.hashed_password = hash_password(user.password)
    db_user = crud.get_by_name(conn.db,user.username)
    if db_user is None:
        if db is None:
            return crud.create(conn.db,user)
        else:
            return crud.create(db,user)
    return db_user

if __name__ == "__main__":
    generate_admin_user()
