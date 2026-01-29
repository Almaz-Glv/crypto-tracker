from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List, Optional
from src.application.services import PriceService
from src.api.dependencies import get_price_service
from src.domain.schemas import PriceTickResponse

router = APIRouter(prefix="/prices", tags=["prices"])


@router.get("/all", response_model=List[PriceTickResponse])
async def get_all_prices(
    ticker: str = Query(..., description="Тикер валюты (например: btc_usd)"),
    limit: Optional[int] = Query(100, description="Лимит записей"),
    service: PriceService = Depends(get_price_service)
):
    """
    Получает все сохраненные данные по указанной валюте.
    
    Пример: /prices/all?ticker=btc_usd&limit=10
    """
    return service.get_all_prices(ticker, limit)


@router.get("/last", response_model=PriceTickResponse)
async def get_last_price(
    ticker: str = Query(..., description="Тикер валюты (например: btc_usd)"),
    service: PriceService = Depends(get_price_service)
):
    """
    Получает последнюю цену валюты.
    
    Пример: /prices/last?ticker=eth_usd
    """
    price = service.get_last_price(ticker)
    if not price:
        raise HTTPException(status_code=404, detail="Price not found")
    return price


@router.get("/filter", response_model=List[PriceTickResponse])
async def get_filtered_prices(
    ticker: str = Query(..., description="Тикер валюты (например: btc_usd)"),
    date_from: Optional[int] = Query(None, description="Начальная дата (UNIX timestamp)"),
    date_to: Optional[int] = Query(None, description="Конечная дата (UNIX timestamp)"),
    service: PriceService = Depends(get_price_service)
):
    """
    Получает цену валюты с фильтром по дате.
    
    Пример: /prices/filter?ticker=btc_usd&date_from=1705618800&date_to=1705705200
    """
    return service.get_prices_by_date_range(ticker, date_from, date_to)
