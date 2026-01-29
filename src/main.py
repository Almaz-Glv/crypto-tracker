from fastapi import FastAPI
from src.core.config import settings
from src.infrastructure.database import init_db
from src.api.routers import prices
import logging

logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="API для отслеживания цен криптовалют с Deribit",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# Регистрируем роутеры
app.include_router(prices.router)


@app.on_event("startup")
async def startup_event():
    """Действия при запуске приложения"""
    logger.info("Starting up...")
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")


@app.on_event("shutdown")
async def shutdown_event():
    """Действия при остановке приложения"""
    logger.info("Shutting down...")


@app.get("/")
async def root():
    """Корневой endpoint"""
    return {
        "message": "Crypto Tracker API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "fetch_prices": "/fetch-prices",
            "prices_all": "/prices/all?ticker=btc_usd",
            "prices_last": "/prices/last?ticker=btc_usd",
            "docs": "/api/docs"
        }
    }


@app.get("/health")
async def health_check():
    """Проверка здоровья"""
    return {"status": "healthy"}


@app.get("/fetch-prices")
async def fetch_prices_manually():
    """Ручной запрос цен (для тестирования)"""
    from src.infrastructure.database import SessionLocal
    from src.application.services import PriceService
    from src.infrastructure.repositories import PriceRepository

    db = SessionLocal()
    try:
        repository = PriceRepository(db)
        service = PriceService(repository)
        results = service.fetch_and_store_prices_sync()

        return {
            "success": True,
            "message": f"Fetched {len(results)} prices",
            "prices": results
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        db.close()
