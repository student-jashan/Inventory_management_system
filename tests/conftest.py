from src.models.user import UserModel
from src.utils.settings import settings
from jose import jwt
from src.utils.security import hash_password
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.main import app
from src.utils.db import Base, get_db


# PostgreSQL test database
TEST_DATABASE_URL = (
    "postgresql://postgres:1234@localhost:5432/inventory_test"
)


# Test database engine
engine = create_engine(
    TEST_DATABASE_URL
)


# Test database session
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


@pytest.fixture
def admin_login_user(db):
    admin = (
        db.query(UserModel)
        .filter(UserModel.email == "testadmin@example.com")
        .first()
    )

    if not admin:
        admin = UserModel(
            full_name="Test Admin",
            email="testadmin@example.com",
            password=hash_password("testpassword"),
            role="Admin"
        )
        db.add(admin)
    else:
        admin.password = hash_password("testpassword")
        admin.role = "Admin"

    db.commit()
    db.refresh(admin)

    return admin

# Create tables before tests
@pytest.fixture(scope="session", autouse=True)
def create_test_database():

    Base.metadata.create_all(bind=engine)

    yield

    # Remove tables after all tests
    Base.metadata.drop_all(bind=engine)


# Database session fixture
@pytest.fixture
def db():

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


# FastAPI TestClient fixture
@pytest.fixture
def client(db):

    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def admin_token(db):

    admin = (
        db.query(UserModel)
        .filter(UserModel.email == "testadmin@example.com")
        .first()
    )

    if not admin:
        admin = UserModel(
            full_name="Test Admin",
            email="testadmin@example.com",
            password=hash_password("testpassword"),
            role="Admin"
        )

        db.add(admin)

    else:
        # Make sure existing test user has a valid password
        admin.password = hash_password("testpassword")
        admin.role = "Admin"

    db.commit()
    db.refresh(admin)

    payload = {
        "sub": str(admin.id),
        "email": admin.email,
        "role": admin.role
    }

    token = jwt.encode(
        payload,
        settings.SECRET_KEY_VALUE,
        algorithm=settings.ALGORITHM
    )

    return token

@pytest.fixture
def sales_executive_token(db):

    sales_executive = (
        db.query(UserModel)
        .filter(UserModel.email == "testsales@example.com")
        .first()
    )

    if not sales_executive:
        sales_executive = UserModel(
            full_name="Test Sales Executive",
            email="testsales@example.com",
            password=hash_password("testpassword"),
            role="Sales Executive"
        )

        db.add(sales_executive)
        db.commit()
        db.refresh(sales_executive)

    payload = {
        "sub": str(sales_executive.id)
    }

    token = jwt.encode(
        payload,
        settings.SECRET_KEY_VALUE,
        algorithm=settings.ALGORITHM
    )

    return token

@pytest.fixture
def inventory_manager_token(db):

    inventory_manager = (
        db.query(UserModel)
        .filter(UserModel.email == "testinventory@example.com")
        .first()
    )

    if not inventory_manager:
        inventory_manager = UserModel(
            full_name="Test Inventory Manager",
            email="testinventory@example.com",
            password=hash_password("testpassword"),
            role="Inventory Manager"
        )

        db.add(inventory_manager)
        db.commit()
        db.refresh(inventory_manager)

    payload = {
        "sub": str(inventory_manager.id)
    }

    token = jwt.encode(
        payload,
        settings.SECRET_KEY_VALUE,
        algorithm=settings.ALGORITHM
    )

    return token

