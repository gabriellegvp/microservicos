from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import os

app = FastAPI()

# Configurações do RabbitMQ (se necessário no futuro)
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")  # Usar "rabbitmq" para Docker Compose
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", 5672))

# Modelo Pydantic para validação de dados
class Product(BaseModel):
    name: str
    price: float
    quantity: int

# Dados em memória (simulando um banco de dados)
products_db = []

@app.get("/products", status_code=status.HTTP_200_OK)
def get_products():
    return {"products": products_db}

@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(product: Product):
    try:
        # Validação automática via Pydantic
        product_dict = product.dict()
        products_db.append(product_dict)
        return {"message": "Product created successfully", "product": product_dict}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating the product: {str(e)}"
        )