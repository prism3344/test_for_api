import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Task
from main import app
from database import Base
from faker import Faker

fake = Faker()

@pytest.fixture
def te_db():
    engine = create_engine('sqlite:///:memory:', echo=False)
    Base.metadata.create_all(bind=engine)
    ses = sessionmaker(bind=engine)
    session = ses()
    yield session

    session.close()
    engine.dispose()


def test_user(te_db):
    
    user = User(username=fake.user_name(), email=fake.email(), hashed_password=fake.password())
    te_db.add(user)
    te_db.commit()
    te_db.refresh(user)
    assert user is not None

def test_task(te_db):
    user = Task(title=fake.user_name(), description=fake.email())
    te_db.add(user)
    te_db.commit()
    te_db.refresh(user)
    assert user is not None