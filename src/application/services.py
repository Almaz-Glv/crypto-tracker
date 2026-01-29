from typing import List, Optional, Dict, Any
import logging
import asyncio
from src.infrastructure.deribit_client import DeribitClient
from src.infrastructure.repositories import PriceRepository
from src.domain.schemas import PriceTickCreate, PriceTickResponse
from src.domain.models import PriceTick

logger = logging.getLogger(__name__)


class PriceService:
    """Сервис для работы с ценами"""
    
    def __init__(self, repository: PriceRepository):
        self.repository = repository
        
    async def fetch_and_store_prices_async(self) -> List[Dict[str, Any]]:
        """
        Асинхронно получает и сохраняет текущие цены с Deribit.
        Использует aiohttp для асинхронных запросов.
        """
        results = []
        client = DeribitClient()
        
        try:
            # Получаем цены для BTC и ETH параллельно
            btc_task = client.get_index_price("BTC")
            eth_task = client.get_index_price("ETH")
            
            btc_data, eth_data = await asyncio.gather(
                btc_task, eth_task, 
                return_exceptions=True
            )
            
            # Обрабатываем BTC
            if isinstance(btc_data, Exception):
                logger.error(f"Error fetching BTC: {btc_data}")
            elif btc_data:
                ticker_data = PriceTickCreate(**btc_data)
                saved = self.repository.create(ticker_data)
                results.append({
                    "ticker": saved.ticker,
                    "price": float(saved.price),
                    "timestamp": saved.timestamp
                })
                logger.info(f"Fetched BTC: ${btc_data['price']:,.2f}")
            
            # Обрабатываем ETH
            if isinstance(eth_data, Exception):
                logger.error(f"Error fetching ETH: {eth_data}")
            elif eth_data:
                ticker_data = PriceTickCreate(**eth_data)
                saved = self.repository.create(ticker_data)
                results.append({
                    "ticker": saved.ticker,
                    "price": float(saved.price),
                    "timestamp": saved.timestamp
                })
                logger.info(f"Fetched ETH: ${eth_data['price']:,.2f}")
                
        except Exception as e:
            logger.error(f"Error in fetch_and_store_prices_async: {e}")
        finally:
            await client.close()
            
        return results
    
    def fetch_and_store_prices_sync(self) -> List[Dict[str, Any]]:
        """
        Синхронная версия для Celery задач.
        Celery не поддерживает асинхронные функции напрямую.
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(self.fetch_and_store_prices_async())
            return result
        finally:
            loop.close()

    def get_all_prices(self, ticker: str, limit: Optional[int] = 100) -> List[PriceTickResponse]:
        """Получает все цены по тикеру"""
        records = self.repository.get_all_by_ticker(ticker, limit)
        return [PriceTickResponse.model_validate(record) for record in records]
    
    def get_last_price(self, ticker: str) -> Optional[PriceTickResponse]:
        """Получает последнюю цену"""
        record = self.repository.get_last_price(ticker)
        if record:
            return PriceTickResponse.from_orm(record)
        return None
    
    def get_prices_by_date_range(
        self, 
        ticker: str, 
        date_from: Optional[int] = None,
        date_to: Optional[int] = None
    ) -> List[PriceTickResponse]:
        """Получает цены за период"""
        records = self.repository.get_by_date_range(ticker, date_from, date_to)
        return [PriceTickResponse.from_orm(record) for record in records]
