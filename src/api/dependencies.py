from fastapi import Depends
from sqlalchemy.orm import Session
from src.infrastructure.database import get_db
from src.infrastructure.repositories import PriceRepository
from src.application.services import PriceService


def get_price_repository(db: Session = Depends(get_db)) -> PriceRepository:
    """Возвращает репозиторий цен"""
    return PriceRepository(db)


def get_price_service(
    repository: PriceRepository = Depends(get_price_repository)
) -> PriceService:
    """Возвращает сервис цен"""
    return PriceService(repository)
