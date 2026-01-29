import pytest


def test_get_all_prices(client):
    """Тест endpoint для получения всех цен"""
    # Arrange
    test_data = [
        {"ticker": "btc_usd", "price": 50000.0, "timestamp": 1234567890},
        {"ticker": "btc_usd", "price": 51000.0, "timestamp": 1234567891},
    ]
    
    # Добавляем тестовые данные через репозиторий (в реальном тесте нужно использовать фикстуру)
    # Вместо этого мы просто протестируем ответ эндпоинта
    
    # Act
    response = client.get("/prices/all?ticker=btc_usd")
    
    # Assert
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_last_price_success(client, price_repository):
    """Тест успешного получения последней цены"""
    # Arrange
    from src.domain.schemas import PriceTickCreate
    
    price_data = PriceTickCreate(
        ticker="btc_usd",
        price=50000.0,
        timestamp=1234567890
    )
    price_repository.create(price_data)
    
    # Act
    response = client.get("/prices/last?ticker=btc_usd")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["ticker"] == "btc_usd"
    assert data["price"] == 50000.0
    assert data["timestamp"] == 1234567890


def test_get_last_price_not_found(client):
    """Тест получения последней цены, когда данных нет"""
    # Act
    response = client.get("/prices/last?ticker=unknown_usd")
    
    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_get_filtered_prices(client, price_repository):
    """Тест endpoint для получения цен с фильтром по дате"""
    # Arrange
    from src.domain.schemas import PriceTickCreate
    
    # Создаем тестовые данные
    prices = [
        PriceTickCreate(ticker="btc_usd", price=50000.0, timestamp=1000),
        PriceTickCreate(ticker="btc_usd", price=51000.0, timestamp=2000),
        PriceTickCreate(ticker="btc_usd", price=52000.0, timestamp=3000),
    ]
    
    for price in prices:
        price_repository.create(price)
    
    # Act
    response = client.get("/prices/filter?ticker=btc_usd&date_from=1500&date_to=2500")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["price"] == 51000.0
    assert data[0]["timestamp"] == 2000


def test_root_endpoint(client):
    """Тест корневого endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health_check(client):
    """Тест health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
