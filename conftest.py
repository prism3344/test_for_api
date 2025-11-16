import pytest
import requests
from faker import Faker

fake = Faker()
@pytest.fixture
def base():
    return 'http://127.0.0.1:8000'
class UserFunc:
    def __init__(self, base):
        self.base = base
        self.username = fake.user_name()
        self.email = fake.email()
        self.password = fake.password()
    def register(self):
        return requests.post(f'{self.base}/register', json={'username': self.username, 'email': self.email, 'password': self.password})
    def login(self):
        return requests.post(f'{self.base}/login', data={'username': self.username, 'email': self.email, 'password': self.password})
    
@pytest.fixture
def header(base):
    u = UserFunc(base)
    reg = u.register()
    log = u.login()
    token = log.json().get('access_token')
    head = {'Authorization': f'Bearer {token}'}
    return head

class Tasks:
    def __init__(self, base, header):
        self.base = base
        self.head = header
        self.title = fake.user_agent()
        self.description = fake.password()
        self.newtitle = fake.email()
        self.newdescription = fake.address()
    def add_task(self):
        return requests.post(f'{self.base}/tasks', json={'title': self.title, 'description': self.description}, headers=self.head)
    
    def get_task_by_id(self, id):
        return requests.get(f'{self.base}/tasks/{id}', headers=self.head)
    
    def edit_task(self, id):
        return requests.put(f'{self.base}/tasks/{id}', json={'title': self.newtitle, 'description': self.newdescription, 'completed': False}, headers=self.head)
    def delete_task(self, id):
        return requests.delete(f'{self.base}/tasks/{id}', headers=self.head)
    
@pytest.fixture
def user(base):
    return UserFunc(base)

@pytest.fixture
def task(base, header):
    return Tasks(base, header)




    


