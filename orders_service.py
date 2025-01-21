from fastapi import FastAPI
import pika

app = FastAPI()

@app.post("/orders")
def create_order(order: dict):
    connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
    channel = connection.channel()
    channel.queue_declare(queue="orders")
    channel.basic_publish(exchange="", routing_key="orders", body=str(order))
    connection.close()
    return {"message": "Order sent to queue", "order": order}

@app.get("/orders")
def get_orders():
    return {"orders": "Endpoint for retrieving orders"}