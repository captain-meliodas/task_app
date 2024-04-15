import pytest
import logging
import json
from fastapi.testclient import TestClient
from pymongo import MongoClient
from src.app import main_app
from src.config.config import Settings
from scripts.generate_admin_user import generate_admin_user
from tests.mocked_data.const import ADMIN_TEST_USER_NAME,ADMIN_TEST_USER_PASSWORD,TASK_PAYLOAD
from src.constants import DELETED_TASK_MSG

app = TestClient(main_app())
settings = Settings.get_settings()

class TestTaskAPI:
    """Test class for testing the task APIs"""
    api_url = "/api/v1/tasks"
    task_id = ""

    @pytest.fixture(scope='module')
    def db_conn(self):
        """This fixture methods establish a db connection and will be available till all tests executed"""

        db_client = MongoClient(
            host=settings.mongo_host,
            port=settings.mongo_port,
            username=settings.mongo_username,
            password=settings.mongo_password
        )
        yield db_client

        tasks_db = db_client[settings.db_name]
        tasks_db.tasks.delete_many({"userId":ADMIN_TEST_USER_NAME})
        tasks_db.users.delete_many({"username":ADMIN_TEST_USER_NAME})

        db_client.close()
    
    @pytest.fixture
    def create_dummy_user(self, db_conn):
        """This fixture will create a admin user for testing the APIs"""

        user = generate_admin_user(db=db_conn[settings.db_name],username=ADMIN_TEST_USER_NAME,password=ADMIN_TEST_USER_PASSWORD)
        logging.info(f"Added dummy admin user for testing APIs")
        return user
    
    @pytest.fixture
    def token(self):
        """This method will generate the auth token for calling CRUD methods on APIs"""

        form_data = {
            "username": ADMIN_TEST_USER_NAME,
            "password": ADMIN_TEST_USER_PASSWORD,
            "scope": "task:read task:write task:delete admin:user"
        }
        
        response = app.post("/api/v1/token",headers={},data=form_data)
        token_data = response.json()
        return token_data['access_token']
    
    def test_create_tasks(self,create_dummy_user,token):
        """This method test the creation of tasks"""
        payload = TASK_PAYLOAD
        headers = {'Authorization': 'Bearer ' + token, "Content-Type": "application/json"}
        response = app.post(f"{self.api_url}",headers=headers,data=json.dumps(payload))
        actual_res = response.json()
        assert actual_res.get("userId") == ADMIN_TEST_USER_NAME
        assert actual_res.get("title") == payload.get("title")
        assert actual_res.get("status") == payload.get("status")
    
    def test_get_tasks(self,create_dummy_user,token):
        """This method test getAll tasks"""
        payload = TASK_PAYLOAD
        headers = {'Authorization': 'Bearer ' + token, "Content-Type": "application/json"}
        response = app.get(f"{self.api_url}",headers=headers)
        actual_res = response.json()
        userId = ""
        title = ""
        status = ""
        for task in actual_res:
            if task.get("userId") == ADMIN_TEST_USER_NAME:
                userId = task.get("userId")
                title = task.get("title")
                status =  task.get("status")
                break
        
        assert userId == ADMIN_TEST_USER_NAME
        assert title == payload.get("title")
        assert status == payload.get("status")
    
    def test_get_task(self,create_dummy_user,token):
        """This method test getAll tasks"""
        payload = TASK_PAYLOAD
        headers = {'Authorization': 'Bearer ' + token, "Content-Type": "application/json"}
        response = app.get(f"{self.api_url}",headers=headers)
        actual_res = response.json()
        _id = ""
        for task in actual_res:
            if task.get("userId") == ADMIN_TEST_USER_NAME:
                _id = task.get("_id")
                break
            
        response = app.get(f"{self.api_url}/{_id}",headers=headers)
        actual_res = response.json()
        userId = actual_res.get("userId")
        title = actual_res.get("title")
        status = actual_res.get("status")
    
        assert userId == ADMIN_TEST_USER_NAME
        assert title == payload.get("title")
        assert status == payload.get("status")
    

    def test_update_task(self,create_dummy_user,token):
        """This method test getAll tasks"""
        payload = TASK_PAYLOAD
        payload['contributors'] = ["dummy_contributor"]
        headers = {'Authorization': 'Bearer ' + token, "Content-Type": "application/json"}
        response = app.get(f"{self.api_url}",headers=headers)
        actual_res = response.json()
        _id = ""
        for task in actual_res:
            if task.get("userId") == ADMIN_TEST_USER_NAME:
                _id = task.get("_id")
                break
            
        response = app.put(f"{self.api_url}/update/{_id}",headers=headers, data=json.dumps(payload))
        actual_res = response.json()
        userId = actual_res.get("userId")
        title = actual_res.get("title")
        status = actual_res.get("status")
    
        assert userId == ADMIN_TEST_USER_NAME
        assert title == payload.get("title")
        assert status == payload.get("status")
        assert actual_res.get('contributors') == ["dummy_contributor"]
    
    def test_remove_task(self,create_dummy_user,token):
        """This method test getAll tasks"""
        payload = TASK_PAYLOAD
        payload['title'] = "New Task"
        headers = {'Authorization': 'Bearer ' + token, "Content-Type": "application/json"}
        response = app.get(f"{self.api_url}",headers=headers)
        actual_res = response.json()
        _id = ""
        for task in actual_res:
            if task.get("userId") == ADMIN_TEST_USER_NAME:
                _id = task.get("_id")
                break
            
        response = app.delete(f"{self.api_url}/delete/{_id}",headers=headers, data=json.dumps(payload))
        actual_res = response.json()
        assert actual_res["message"] == DELETED_TASK_MSG.format(_id)
    


