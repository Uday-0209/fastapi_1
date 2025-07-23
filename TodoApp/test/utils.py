from sqlalchemy import create_engine, text
from sqlalchemy import StaticPool
from ..database import Base
from ..main import app
from fastapi.testclient import TestClient
import pytest
from ..models import Todos, users
from sqlalchemy.orm import sessionmaker, declarative_base
from ..routers.auth import bcrypt_context

SQLALCHEMY_DATABASE_URL = 'sqlite:///./testdb.db'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={'check_same_thread': False},
    poolclass = StaticPool
)

TestingSessionLocal = sessionmaker(autocommit = False, autoflush = False, bind=engine)

Base.metadata.create_all(bind = engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {'username':'codingwithuk', 'id':1, 'user_role':'admin'}

client = TestClient(app)

@pytest.fixture
def test_todo():
    todo = Todos(
        title = "Learn to code!",
        description="Need to learn today",
        priority = '5', #bcz we mentioned in the models as str for priority
        complete = False,
        owner_id = 1
    )
    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()




@pytest.fixture
def test_user():
    user = users(
        username = "codingwithuk",
        email = "udayhiremath02@gmail.com",
        first_name = 'Uday',
        last_name = 'Hiremath',
        hashed_password = bcrypt_context.hash('testpassword'),
        role = 'admin',
        phone_number = '8310215305'
    )
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text('DELETE FROM users;'))
        connection.commit()