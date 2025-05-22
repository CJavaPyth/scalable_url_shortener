#!/bin/sh
# wait-for-db.sh

# You can modify the host/port or use env vars if needed
until pg_isready -h db -p 5432; do
  echo "Waiting for Postgres at db:5432..."
  sleep 2
done

echo "Postgres is ready. Starting app..."
exec uvicorn main:app --host 0.0.0.0 --port 8000
