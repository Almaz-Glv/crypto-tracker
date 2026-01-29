#!/bin/bash

set -e

echo "========================================"
echo "Starting Crypto Tracker Application"
echo "========================================"

# Ждем PostgreSQL
echo "Waiting for PostgreSQL..."
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q'; do
  sleep 2
done

echo "✅ PostgreSQL is ready"

# Инициализация БД
echo "Initializing database..."
python -c "
import sys
sys.path.append('.')
from src.infrastructure.database import init_db
init_db()
print('✅ Database initialized')
"

# Запускаем Celery worker
echo "Starting Celery worker..."
celery -A src.infrastructure.celery_app.celery_app worker \
  --loglevel=info \
  --pool=solo \
  --concurrency=1 \
  --detach  # В фоне

# Запускаем Celery beat
echo "Starting Celery beat..."
celery -A src.infrastructure.celery_app.celery_app beat \
  --loglevel=info \
  --detach  # В фоне

# Запускаем FastAPI
echo "Starting FastAPI on port 8000..."
exec uvicorn src.main:app --host 0.0.0.0 --port 8000#!/bin/bash

set -e

echo "========================================"
echo "Starting Crypto Tracker Application"
echo "========================================"

# Ждем PostgreSQL
echo "Waiting for PostgreSQL..."
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q'; do
  sleep 2
done

echo "✅ PostgreSQL is ready"

# Инициализация БД
echo "Initializing database..."
python -c "
import sys
sys.path.append('.')
from src.infrastructure.database import init_db
init_db()
print('✅ Database initialized')
"

# Запускаем Celery worker
echo "Starting Celery worker..."
celery -A src.infrastructure.celery_app.celery_app worker \
  --loglevel=info \
  --pool=solo \
  --concurrency=1 \
  --detach  # В фоне

# Запускаем Celery beat
echo "Starting Celery beat..."
celery -A src.infrastructure.celery_app.celery_app beat \
  --loglevel=info \
  --detach  # В фоне

# Запускаем FastAPI
echo "Starting FastAPI on port 8000..."
exec uvicorn src.main:app --host 0.0.0.0 --port 8000
