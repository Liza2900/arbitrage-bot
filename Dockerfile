FROM python:3.11-slim

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 10000

CMD ["uvicorn", "arbitrage_bot_fastapi:app", "--host", "0.0.0.0", "--port", "10000"]
