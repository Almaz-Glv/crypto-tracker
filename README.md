# crypto-tracker

Все команды выполняют в каталоге где храниться основной main
и запустить виртуальное окружение
sourse venv/script/activate

Сначала нужно запустить PostgreSQL

docker start crypto-postgres
docker ps | grep crypto-postgres (Проверить, запущено ли оно уже)

Запуск FastAPI сервера
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000


Команды для проверки работаспособности API
curl http://localhost:8000/health
curl http://localhost:8000/prices/last?ticker=btc_usd