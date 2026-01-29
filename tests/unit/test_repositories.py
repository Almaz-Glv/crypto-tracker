import pytest
from src.domain.schemas import PriceTickCreate
from src.domain.models import PriceTick


def test_create_price_tick(price_repository):
    """Тест создания записи о цене"""
    # Arrange
    price_data = PriceTickCreate(
        ticker="btc_usd",
        price=50000.0,
        timestamp=1234567890
    )
    
    # Act
    result = price_repository.create(price_data)
    
    # Assert
    assert result.id is not None
    assert result.ticker == "btc_usd"
    assert float(result.price) == 50000.0
    assert result.timestamp == 1234567890


def test_get_all_by_ticker(price_repository, clean_db):
    """Тест получения всех записей по тикеру"""
    # Arrange - clean_db автоматически очистит БД
    price_data1 = PriceTickCreate(ticker="btc_usd", price=50000.0, timestamp=1234567890)
    price_data2 = PriceTickCreate(ticker="btc_usd", price=51000.0, timestamp=1234567891)
    price_data3 = PriceTickCreate(ticker="eth_usd", price=3000.0, timestamp=1234567890)
    
    price_repository.create(price_data1)
    price_repository.create(price_data2)
    price_repository.create(price_data3)
    
    # Act
    btc_prices = price_repository.get_all_by_ticker("btc_usd")
    eth_prices = price_repository.get_all_by_ticker("eth_usd")
    
    # Assert
    assert len(btc_prices) == 2
    assert len(eth_prices) == 1
    assert btc_prices[0].ticker == "btc_usd"
    assert eth_prices[0].ticker == "eth_usd"


def test_get_last_price(price_repository):
    """Тест получения последней цены"""
    # Arrange
    price_data1 = PriceTickCreate(ticker="btc_usd", price=50000.0, timestamp=1234567890)
    price_data2 = PriceTickCreate(ticker="btc_usd", price=51000.0, timestamp=1234567891)
    
    price_repository.create(price_data1)
    price_repository.create(price_data2)
    
    # Act
    last_price = price_repository.get_last_price("btc_usd")
    
    # Assert
    assert last_price is not None
    assert float(last_price.price) == 51000.0
    assert last_price.timestamp == 1234567891


def test_get_by_date_range(price_repository):
    """Тест получения записей за период"""
    # Arrange
    price_data1 = PriceTickCreate(ticker="btc_usd", price=50000.0, timestamp=1000)
    price_data2 = PriceTickCreate(ticker="btc_usd", price=51000.0, timestamp=2000)
    price_data3 = PriceTickCreate(ticker="btc_usd", price=52000.0, timestamp=3000)
    
    price_repository.create(price_data1)
    price_repository.create(price_data2)
    price_repository.create(price_data3)
    
    # Act
    prices_in_range = price_repository.get_by_date_range("btc_usd", date_from=1500, date_to=2500)
    
    # Assert
    assert len(prices_in_range) == 1
    assert float(prices_in_range[0].price) == 51000.0
    assert prices_in_range[0].timestamp == 2000


def test_duplicate_timestamp_not_created(price_repository):
    """Тест, что запись с одинаковым timestamp не дублируется"""
    # Arrange
    price_repository.db.query(PriceTick).delete()
    price_repository.db.commit()
    
    price_data = PriceTickCreate(
        ticker="btc_usd",
        price=50000.0,
        timestamp=1234567890
    )
    
    # Act
    result1 = price_repository.create(price_data)
    result2 = price_repository.create(price_data)  # Пытаемся создать с тем же timestamp
    
    # Assert
    assert result1.id == result2.id  # Должен вернуть существующую запись
    assert price_repository.db.query(PriceTick).count() == 1  # Должна быть только одна запись

