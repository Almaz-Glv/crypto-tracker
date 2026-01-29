import aiohttp
import asyncio
import logging
from typing import Dict, Any, Optional
from src.core.config import settings
import time

logger = logging.getLogger(__name__)


class DeribitClient:
    """Асинхронный клиент для Deribit API"""
    
    def __init__(self):
        self.base_url = settings.deribit_base_url
        self.session: Optional[aiohttp.ClientSession] = None
        
    async def _get_session(self) -> aiohttp.ClientSession:
        """Создает или возвращает существующую сессию"""
        if self.session is None or self.session.closed:
            timeout = aiohttp.ClientTimeout(total=10)
            self.session = aiohttp.ClientSession(timeout=timeout)
        return self.session
    
    async def get_index_price(self, currency: str) -> Optional[Dict[str, Any]]:
        """
        Получает реальную цену с Deribit API.
        
        Args:
            currency: BTC или ETH
            
        Returns:
            Словарь с данными или None при ошибке
        """
        try:
            session = await self._get_session()
            url = f"{self.base_url}/public/get_index_price"
            params = {"index_name": f"{currency.lower()}_usd"}
            
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    if "error" in data and data["error"]:
                        logger.error(f"Deribit API error: {data['error']}")
                        return None
                    
                    result = data.get("result", {})
                    
                    return {
                        "ticker": f"{currency.lower()}_usd",
                        "price": float(result.get("index_price", 0)),
                        "timestamp": int(time.time())
                    }
                else:
                    logger.error(f"HTTP error: {response.status}")
                    return None
                    
        except Exception as e:
            logger.error(f"Error fetching {currency} price: {e}")
            return None
    
    async def close(self):
        """Закрывает сессию"""
        if self.session and not self.session.closed:
            await self.session.close()
