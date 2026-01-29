from pydantic import BaseModel, Field, validator, ConfigDict
from typing import Optional
from datetime import datetime


class PriceTickBase(BaseModel):
    ticker: str = Field(..., example="btc_usd", min_length=3, max_length=10)
    price: float = Field(..., gt=0, example=45000.50)
    timestamp: int = Field(..., gt=0, example=1705672800)


class PriceTickCreate(PriceTickBase):
    """Схема для создания записи"""
    pass


class PriceTickResponse(PriceTickBase):
    """Схема для ответа API"""
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class PriceFilter(BaseModel):
    """Схема для фильтрации цен"""
    ticker: str = Field(..., example="btc_usd")
    date_from: Optional[int] = Field(None, description="UNIX timestamp начала периода")
    date_to: Optional[int] = Field(None, description="UNIX timestamp конца периода")
    
    @validator('date_to')
    def validate_dates(cls, date_to, values):
        if date_to and 'date_from' in values and values['date_from']:
            if date_to < values['date_from']:
                raise ValueError('date_to должен быть больше или равен date_from')
        return date_to
