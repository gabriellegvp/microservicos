from fastapi import FastAPI, HTTPException, status, Query
from pydantic import BaseModel, Field
from typing import List, Optional
import pika
import os
import json
from uuid import uuid4

app = FastAPI(
    title="Order Management API",
    description="API para gerenciamento de pedidos com integração ao RabbitMQ",
    version="1.0.0",
)

# Configurações do RabbitMQ
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")  # Usar "rabbitmq" para Docker Compose
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", 5672))
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "guest")

# Modelo Pydantic para validação de dados
class OrderItem(BaseModel):
    product_id: str = Field(..., min_length=1, description="ID do produto")
    quantity: int = Field(..., gt=0, description="Quantidade do produto")

class Order(BaseModel):
    order_id: str = Field(default_factory=lambda: str(uuid4()), description="ID único do pedido")
    customer_name: str = Field(..., min_length=1, max_length=100, description="Nome do cliente")
    items: List[OrderItem] = Field(..., description="Lista de itens do pedido")

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

@app.post("/orders", response_model=Order, status_code=status.HTTP_201_CREATED)
def create_order(order: Order):
    try:
        # Converte o modelo Pydantic para dicionário
        order_dict = order.dict()
        # Publica a ordem na fila "orders"
        publish_to_queue("orders", order_dict)
        return {"message": "Order sent to queue", "order": order_dict}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/orders", response_model=List[Order], status_code=status.HTTP_200_OK)
def get_orders():
    # Simulação de retorno de pedidos (em um cenário real, isso viria de um banco de dados)
    return []

@app.get("/orders/{order_id}", response_model=Order, status_code=status.HTTP_200_OK)
def get_order(order_id: str):
    # Simulação de busca de pedido por ID (em um cenário real, isso viria de um banco de dados)
    order = next((order for order in get_orders() if order["order_id"] == order_id), None)
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    return order

# Endpoint para processar pedidos (simulação de consumo da fila)
@app.post("/orders/process", status_code=status.HTTP_200_OK)
def process_orders():
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
        channel.queue_declare(queue="orders", durable=True)

        # Função de callback para processar mensagens
        def callback(ch, method, properties, body):
            order = json.loads(body)
            print(f" [x] Processing order: {order}")
            # Aqui você pode adicionar a lógica para processar o pedido
            # Por exemplo, salvar no banco de dados ou enviar uma confirmação
            ch.basic_ack(delivery_tag=method.delivery_tag)  # Confirma o processamento

        # Configura o consumo da fila
        channel.basic_consume(queue="orders", on_message_callback=callback)

        print(" [*] Waiting for orders. To exit press CTRL+C")
        channel.start_consuming()
    except pika.exceptions.AMQPConnectionError as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect to RabbitMQ: {str(e)}")
    finally:
        # Fecha a conexão
        if connection and not connection.is_closed:
            connection.close()

    return {"message": "Orders processed successfully"}