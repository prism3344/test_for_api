from database import Base, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from main import app
import pytest
from faker import Faker
from main import get_db as get_db_original # Importuj oryginalną funkcję z main.py
SQL_URL = 'sqlite:///./testtin.db'
engine = create_engine(SQL_URL, echo=False)
Base.metadata.create_all(bind=engine)
ses = sessionmaker(bind=engine)


def overrides_get_db():
    db = ses()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db_original] = overrides_get_db

client = TestClient(app)

fake = Faker()
@pytest.fixture
def username():
    return fake.user_name()

@pytest.fixture
def email():
    return fake.email()

@pytest.fixture
def password():
    return fake.password()

@pytest.fixture
def header(username, email, password):
    res = client.post('/register', json={'username': username, 'email': email, 'password': password})
    log = client.post('/login', data={'username': username, 'email': email, 'password': password})
    token = log.json().get('access_token')
    head = {'Authorization': f'Bearer {token}'}
    return head

def test_add_task(header, username, email):
    add = client.post('/tasks', json={'title': username, 'description': email}, headers=header)
    assert add.status_code == 200
    pid = add.json().get('id')
    gettask = client.get(f'/tasks/{pid}', headers=header)
    des = add.json().get('description')
    tit = add.json().get('title')
    assert gettask.json() == {'completed': False, 'description': des, 'id': pid, 'title': tit}

def test_edit(header, username, email):
    add = client.post('/tasks', json={'title': username, 'description': email, 'completed': False}, headers=header)
    pid = add.json().get('id')
    edit = client.put(f'/tasks/{pid}', json={'title': username, 'description': email, 'completed': False}, headers=header)
    assert edit.status_code == 200




