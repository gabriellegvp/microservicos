from fastapi import FastAPI
import pika
import os

app = FastAPI()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", 5672))

@app.post("/orders")
def create_order(order: dict):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT))
    channel = connection.channel()
    channel.queue_declare(queue="orders")
    channel.basic_publish(exchange="", routing_key="orders", body=str(order))
    connection.close()
    return {"message": "Order sent to queue", "order": order}

FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["uvicorn", "users_service:app", "--host", "0.0.0.0", "--port", "8001"]