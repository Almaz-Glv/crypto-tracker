from sqlalchemy import Column, Integer, String, Numeric, DateTime
from sqlalchemy.sql import func
from src.infrastructure.database import Base


class PriceTick(Base):
    __tablename__ = "price_ticks"
    
    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(10), nullable=False, index=True)
    price = Column(Numeric(12, 2), nullable=False)
    timestamp = Column(Integer, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<PriceTick(ticker='{self.ticker}', price={self.price}, timestamp={self.timestamp})>"
