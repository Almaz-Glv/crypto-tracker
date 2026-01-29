import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.infrastructure.database import Base, get_db
from src.main import app


# Тестовая база данных в памяти
TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="function")  # Изменено с session на function
def engine():
    """Фикстура для создания тестового движка БД"""
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def session(engine):
    """Фикстура для тестовой сессии БД с изоляцией транзакций"""
    connection = engine.connect()
    transaction = connection.begin()
    
    TestingSessionLocal = sessionmaker(
        autocommit=False, 
        autoflush=False, 
        bind=connection
    )
    
    db = TestingSessionLocal()
    
    try:
        yield db
    finally:
        db.close()
        transaction.rollback()  # Откатываем изменения после теста
        connection.close()


@pytest.fixture
def client(session):
    """Фикстура для тестового клиента FastAPI"""
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    test_client = TestClient(app)
    yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def price_repository(session):
    """Фикстура для репозитория цен"""
    from src.infrastructure.repositories import PriceRepository
    return PriceRepository(session)


@pytest.fixture(scope="function")
def clean_db(session):
    """Фикстура для очистки базы данных перед каждым тестом"""
    from src.domain.models import PriceTick
    session.query(PriceTick).delete()
    session.commit()
    yield
    session.query(PriceTick).delete()
    session.commit()
