from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Database
    postgres_user: str = "user"
    postgres_password: str = "password"
    postgres_db: str = "crypto_tracker"
    postgres_host: str = "localhost"
    postgres_port: str = "5432"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # Deribit
    deribit_base_url: str = "https://deribit.com/api/v2"

    # App
    app_name: str = "Crypto Tracker API"
    debug: bool = True
    log_level: str = "INFO"

    @property
    def database_url(self) -> str:
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
