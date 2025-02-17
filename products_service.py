from fastapi import FastAPI, HTTPException, status, Query
from pydantic import BaseModel, Field
from typing import List, Optional
import os
from uuid import uuid4

app = FastAPI(
    title="Product Management API",
    description="API para gerenciamento de produtos",
    version="1.0.0",
)

# Configurações do RabbitMQ (se necessário no futuro)
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")  # Usar "rabbitmq" para Docker Compose
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", 5672))

# Modelo Pydantic para validação de dados
class Product(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0)
    quantity: int = Field(..., ge=0)

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    price: Optional[float] = Field(None, gt=0)
    quantity: Optional[int] = Field(None, ge=0)

# Dados em memória (simulando um banco de dados)
products_db = []

@app.get("/products", response_model=List[Product], status_code=status.HTTP_200_OK)
def get_products():
    return products_db

@app.get("/products/{product_id}", response_model=Product, status_code=status.HTTP_200_OK)
def get_product(product_id: str):
    product = next((product for product in products_db if product["id"] == product_id), None)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product

@app.post("/products", response_model=Product, status_code=status.HTTP_201_CREATED)
def create_product(product: Product):
    try:
        product_dict = product.dict()
        products_db.append(product_dict)
        return product_dict
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating the product: {str(e)}"
        )

@app.put("/products/{product_id}", response_model=Product, status_code=status.HTTP_200_OK)
def update_product(product_id: str, product_update: ProductUpdate):
    product = next((product for product in products_db if product["id"] == product_id), None)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    try:
        update_data = product_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            product[key] = value
        return product
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while updating the product: {str(e)}"
        )

@app.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: str):
    product = next((product for product in products_db if product["id"] == product_id), None)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    try:
        products_db.remove(product)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while deleting the product: {str(e)}"
        )

# Endpoint para busca de produtos por nome
@app.get("/products/search/", response_model=List[Product], status_code=status.HTTP_200_OK)
def search_products(
    name: Optional[str] = Query(None, min_length=1, max_length=100)
):
    if name:
        results = [product for product in products_db if name.lower() in product["name"].lower()]
        return results
    return products_db

# Endpoint para listagem paginada de produtos
@app.get("/products/paginated/", response_model=List[Product], status_code=status.HTTP_200_OK)
def get_paginated_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    return products_db[skip:skip + limit]