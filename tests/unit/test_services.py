import pytest
from unittest.mock import Mock
from datetime import datetime, timezone
from src.application.services import PriceService
from src.domain.schemas import PriceTickCreate


def create_mock_record(ticker="btc_usd", price=50000.0, timestamp=1234567890):
    """Создает мок-запись с правильными атрибутами"""
    mock_record = Mock()
    mock_record.id = 1
    mock_record.ticker = ticker
    mock_record.price = price
    mock_record.timestamp = timestamp
    mock_record.created_at = datetime.now(timezone.utc)  # Важно!
    return mock_record


@pytest.fixture
def mock_repository():
    """Фикстура для мок-репозитория"""
    return Mock()


@pytest.fixture
def price_service(mock_repository):
    """Фикстура для сервиса с мок-репозиторием"""
    return PriceService(mock_repository)


def test_get_all_prices(price_service, mock_repository):
    """Тест получения всех цен через сервис"""
    # Arrange
    mock_record = create_mock_record()
    
    mock_repository.get_all_by_ticker.return_value = [mock_record]
    
    # Act
    result = price_service.get_all_prices("btc_usd", limit=10)
    
    # Assert
    assert len(result) == 1
    assert result[0].ticker == "btc_usd"
    assert result[0].price == 50000.0
    mock_repository.get_all_by_ticker.assert_called_once_with("btc_usd", 10)


def test_get_last_price(price_service, mock_repository):
    """Тест получения последней цены через сервис"""
    # Arrange
    mock_record = create_mock_record()
    
    mock_repository.get_last_price.return_value = mock_record
    
    # Act
    result = price_service.get_last_price("btc_usd")
    
    # Assert
    assert result is not None
    assert result.ticker == "btc_usd"
    assert result.price == 50000.0
    mock_repository.get_last_price.assert_called_once_with("btc_usd")


def test_get_last_price_none(price_service, mock_repository):
    """Тест получения последней цены, когда ее нет"""
    # Arrange
    mock_repository.get_last_price.return_value = None
    
    # Act
    result = price_service.get_last_price("btc_usd")
    
    # Assert
    assert result is None
    mock_repository.get_last_price.assert_called_once_with("btc_usd")


def test_get_prices_by_date_range(price_service, mock_repository):
    """Тест получения цен за период через сервис"""
    # Arrange
    mock_record = create_mock_record()
    
    mock_repository.get_by_date_range.return_value = [mock_record]
    
    # Act
    result = price_service.get_prices_by_date_range(
        "btc_usd", 
        date_from=1234567800,
        date_to=1234567900
    )
    
    # Assert
    assert len(result) == 1
    assert result[0].ticker == "btc_usd"
    mock_repository.get_by_date_range.assert_called_once_with(
        "btc_usd", 1234567800, 1234567900
    )