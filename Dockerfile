FROM python:3.12

WORKDIR /app

COPY [^logs]* /app
COPY alembic/ /app/alembic
COPY sql/ /app/sql

RUN pip install --no-cache-dir -r requirements.txt