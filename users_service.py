from fastapi import FastAPI

app = FastAPI()

@app.get("/users")
def get_users():
    return {"users": ["user1", "user2"]}

@app.post("/users")
def create_user(user: dict):
    return {"message": "User created successfully", "user": user}