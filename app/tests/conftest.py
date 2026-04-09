import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app
from app.core.security import hash_password
from app.models.user import User
from app.models.product import Product

# Banco de testes em memória
SQLALCHEMY_TEST_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_TEST_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def setup_db():
    """Cria tabelas antes de cada teste e limpa depois"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db():
    """Sessão de banco para testes"""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(db):
    """Client HTTP que usa o banco de testes"""
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db) -> User:
    """Cria usuário comum para testes"""
    user = User(
        email="user@test.com",
        name="Test User",
        number="123456789",
        password=hash_password("Test1234"),
        isadmin=False,
        active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def test_admin(db) -> User:
    """Cria admin para testes"""
    admin = User(
        email="admin@test.com",
        name="Test Admin",
        number="987654321",
        password=hash_password("Admin1234"),
        isadmin=True,
        active=True
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin


@pytest.fixture
def user_token(client, test_user) -> str:
    """Token JWT de usuário comum"""
    response = client.post("/auth/login", json={
        "email": "user@test.com",
        "password": "Test1234"
    })
    return response.json()["access_token"]


@pytest.fixture
def admin_token(client, test_admin) -> str:
    """Token JWT de admin"""
    response = client.post("/auth/login", json={
        "email": "admin@test.com",
        "password": "Admin1234"
    })
    return response.json()["access_token"]


@pytest.fixture
def auth_header(user_token) -> dict:
    """Header de autenticação de usuário"""
    return {"Authorization": f"Bearer {user_token}"}


@pytest.fixture
def admin_header(admin_token) -> dict:
    """Header de autenticação de admin"""
    return {"Authorization": f"Bearer {admin_token}"}


@pytest.fixture
def test_product(db) -> Product:
    """Cria produto para testes"""
    product = Product(
        name="Test Product",
        description="A test product",
        price=49.90,
        stock=100,
        category="test",
        active=True
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product