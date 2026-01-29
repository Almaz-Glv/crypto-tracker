from celery import shared_task
import logging
from src.infrastructure.database import SessionLocal
from src.application.services import PriceService
from src.infrastructure.repositories import PriceRepository
import time

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def fetch_and_store_prices_task(self):
    """
    Celery задача для получения и сохранения цен каждую минуту.
    """
    task_id = self.request.id
    logger.info(f"[Task {task_id}] Starting fetch_and_store_prices_task")
    
    db = SessionLocal()
    try:
        repository = PriceRepository(db)
        service = PriceService(repository)
        
        # ИСПРАВЛЕНО: используем синхронную версию
        start_time = time.time()
        results = service.fetch_and_store_prices_sync()  # Было: fetch_and_store_prices()
        elapsed_time = time.time() - start_time
        
        logger.info(f"[Task {task_id}] Successfully fetched {len(results)} prices in {elapsed_time:.2f}s")
        
        return {
            "task_id": task_id,
            "status": "success",
            "timestamp": time.time(),
            "prices_fetched": len(results),
            "prices": results,
            "execution_time": elapsed_time
        }
        
    except Exception as e:
        logger.error(f"[Task {task_id}] Failed to fetch prices: {str(e)}")
        
        # Повторяем задачу через 30 секунд при ошибке
        raise self.retry(exc=e, countdown=30)
        
    finally:
        db.close()


@shared_task
def test_task(message: str = "Hello from Celery"):
    """
    Тестовая задача для проверки работы Celery.
    """
    logger.info(f"Test task received: {message}")
    return {
        "status": "success",
        "message": message,
        "timestamp": time.time()
    }
