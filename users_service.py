from fastapi import FastAPI, HTTPException, status, Query
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
import os
from uuid import uuid4

app = FastAPI(
    title="User Management API",
    description="API para gerenciamento de usuários",
    version="1.0.0",
)

# Configurações do RabbitMQ (se necessário no futuro)
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")  # Usar "rabbitmq" para Docker Compose
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", 5672))

# Modelo Pydantic para validação de dados
class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    age: int = Field(..., gt=0, lt=120)

class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    email: Optional[EmailStr] = None
    age: Optional[int] = Field(None, gt=0, lt=120)

# Dados em memória (simulando um banco de dados)
users_db = []

@app.get("/users", response_model=List[User], status_code=status.HTTP_200_OK)
def get_users():
    return users_db

@app.get("/users/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
def get_user(user_id: str):
    user = next((user for user in users_db if user["id"] == user_id), None)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: User):
    try:
        user_dict = user.dict()
        users_db.append(user_dict)
        return user_dict
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating the user: {str(e)}"
        )

@app.put("/users/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
def update_user(user_id: str, user_update: UserUpdate):
    user = next((user for user in users_db if user["id"] == user_id), None)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    try:
        update_data = user_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            user[key] = value
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while updating the user: {str(e)}"
        )

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str):
    user = next((user for user in users_db if user["id"] == user_id), None)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    try:
        users_db.remove(user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while deleting the user: {str(e)}"
        )

# Endpoint para busca de usuários por nome ou email
@app.get("/users/search/", response_model=List[User], status_code=status.HTTP_200_OK)
def search_users(
    name: Optional[str] = Query(None, min_length=1, max_length=50),
    email: Optional[EmailStr] = None
):
    results = users_db
    if name:
        results = [user for user in results if name.lower() in user["name"].lower()]
    if email:
        results = [user for user in results if user["email"] == email]
    return results