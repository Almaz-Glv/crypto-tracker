from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_
from src.domain.models import PriceTick
from src.domain.schemas import PriceTickCreate
import logging

logger = logging.getLogger(__name__)


class PriceRepository:
    """Репозиторий для работы с ценами"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, price_data: PriceTickCreate) -> PriceTick:
        """Создает запись о цене"""
        try:
            # Проверяем, нет ли уже записи с таким timestamp
            existing = self.db.query(PriceTick).filter(
                and_(
                    PriceTick.ticker == price_data.ticker,
                    PriceTick.timestamp == price_data.timestamp
                )
            ).first()
            
            if existing:
                logger.debug(f"Record already exists: {price_data.ticker} at {price_data.timestamp}")
                return existing
            
            db_price = PriceTick(
                ticker=price_data.ticker,
                price=price_data.price,
                timestamp=price_data.timestamp
            )
            
            self.db.add(db_price)
            self.db.commit()
            self.db.refresh(db_price)
            
            logger.info(f"Created price record: {db_price.ticker} = ${db_price.price}")
            return db_price
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to create price record: {e}")
            raise
    
    def get_all_by_ticker(self, ticker: str, limit: Optional[int] = 100) -> List[PriceTick]:
        """Получает все записи по тикеру"""
        return self.db.query(PriceTick)\
            .filter(PriceTick.ticker == ticker)\
            .order_by(desc(PriceTick.timestamp))\
            .limit(limit)\
            .all()
    
    def get_last_price(self, ticker: str) -> Optional[PriceTick]:
        """Получает последнюю цену"""
        return self.db.query(PriceTick)\
            .filter(PriceTick.ticker == ticker)\
            .order_by(desc(PriceTick.timestamp))\
            .first()
    
    def get_by_date_range(
        self, 
        ticker: str, 
        date_from: Optional[int] = None,
        date_to: Optional[int] = None
    ) -> List[PriceTick]:
        """Получает записи за период"""
        query = self.db.query(PriceTick).filter(PriceTick.ticker == ticker)
        
        if date_from:
            query = query.filter(PriceTick.timestamp >= date_from)
        if date_to:
            query = query.filter(PriceTick.timestamp <= date_to)
        
        return query.order_by(desc(PriceTick.timestamp)).all()
