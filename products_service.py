from fastapi import FastAPI
import os

app = FastAPI()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT", 5672)

@app.get("/products")
def get_products():
    return {"products": ["product1", "product2"]}

@app.post("/products")
def create_product(product: dict):
    return {"message": "Product created successfully", "product": product}

FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["uvicorn", "products_service:app", "--host", "0.0.0.0", "--port", "8002"]