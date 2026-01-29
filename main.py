from fastapi import FastAPI
from src.core.config import settings
from src.infrastructure.database import init_db
import logging

# Настройка логирования
logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Создание приложения FastAPI
app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="API для отслеживания цен криптовалют с Deribit",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)


@app.on_event("startup")
async def startup_event():
    """
    Действия при запуске приложения.
    """
    logger.info("Starting up...")
    # Инициализация базы данных
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Действия при остановке приложения.
    """
    logger.info("Shutting down...")


@app.get("/")
async def root():
    """
    Корневой endpoint для проверки работы API.
    """
    return {
        "message": "Crypto Tracker API",
        "version": "1.0.0",
        "docs": "/api/docs"
    }


@app.get("/health")
async def health_check():
    """
    Endpoint для проверки здоровья приложения.
    """
    return {"status": "healthy"}
