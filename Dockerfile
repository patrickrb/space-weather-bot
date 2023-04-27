FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN apt-get update && \
    apt-get install -y build-essential && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY spaceweatherbot.py .
COPY .env .
