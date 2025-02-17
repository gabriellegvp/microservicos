from fastapi import FastAPI, HTTPException
import pika
import os
import json

app = FastAPI()

# Configurações do RabbitMQ
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")  # Usar "rabbitmq" para Docker Compose
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", 5672))
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "guest")

# Função para publicar mensagens no RabbitMQ
def publish_to_queue(queue_name: str, message: dict):
    try:
        # Conecta ao RabbitMQ
        credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=RABBITMQ_HOST,
                port=RABBITMQ_PORT,
                credentials=credentials
            )
        )
        channel = connection.channel()

        # Declara a fila (se não existir)
        channel.queue_declare(queue=queue_name, durable=True)  # Fila durável para persistência

        # Publica a mensagem
        channel.basic_publish(
            exchange="",
            routing_key=queue_name,
            body=json.dumps(message),  # Converte o dicionário para JSON
            properties=pika.BasicProperties(
                delivery_mode=2,  # Torna a mensagem persistente
            )
        )
        print(f" [x] Sent {message} to {queue_name}")
    except pika.exceptions.AMQPConnectionError as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect to RabbitMQ: {str(e)}")
    finally:
        # Fecha a conexão
        if connection and not connection.is_closed:
            connection.close()

@app.post("/orders")
def create_order(order: dict):
    try:
        # Publica a ordem na fila "orders"
        publish_to_queue("orders", order)
        return {"message": "Order sent to queue", "order": order}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))