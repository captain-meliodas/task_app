from src.database.connection import DbConnection
from src.database.crud import MongoUserCrud
from src.routes.users import hash_password
from src.models.schemas import UserCreate

conn = DbConnection()
crud = MongoUserCrud()


def main():
    """method to create an admin user"""

    user = UserCreate(username="ankitsingh",email="email",scopes=[
            'task:read',
            'task:write',
            'task:delete',
            'admin:user'
        ],created_by="script", password="AnkitSingh@23021995")
    
    user.hashed_password = hash_password(user.password)
    db_user = crud.get_by_name(conn.db,user.username)
    if db_user is None:
        crud.create(conn.db,user)

if __name__ == "__main__":
    main()
