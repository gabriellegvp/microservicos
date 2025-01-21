from fastapi import FastAPI
import os

app = FastAPI()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT", 5672)

@app.get("/users")
def get_users():
    return {"users": ["user1", "user2"]}

@app.post("/users")
def create_user(user: dict):
    return {"message": "User created successfully", "user": user}

FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["uvicorn", "orders_service:app", "--host", "0.0.0.0", "--port", "8003"]