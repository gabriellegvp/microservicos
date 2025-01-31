from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import os

app = FastAPI()

# Configurações do RabbitMQ (se necessário no futuro)
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")  # Usar "rabbitmq" para Docker Compose
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", 5672))

# Modelo Pydantic para validação de dados
class User(BaseModel):
    name: str
    email: str
    age: int

# Dados em memória (simulando um banco de dados)
users_db = []

@app.get("/users", status_code=status.HTTP_200_OK)
def get_users():
    return {"users": users_db}

@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: User):
    try:
        # Validação automática via Pydantic
        user_dict = user.dict()
        users_db.append(user_dict)
        return {"message": "User created successfully", "user": user_dict}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating the user: {str(e)}"
        )