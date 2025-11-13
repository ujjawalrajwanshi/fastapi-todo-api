from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="My First API", version="1.0.0")

# Request model
class User(BaseModel):
    name: str
    age: int
    email: Optional[str] = None

# Response model
class UserResponse(User):
    id: int
    message: str

# In-memory storage (like a simple database)
users = []
user_id_counter = 1

@app.get("/")
def root():
    return {"message": "User API is running", "total_users": len(users)}

@app.post("/users", response_model=UserResponse)
def create_user(user: User):
    global user_id_counter
    new_user = {
        "id": user_id_counter,
        "name": user.name,
        "age": user.age,
        "email": user.email
    }
    users.append(new_user)
    user_id_counter += 1
    
    return {**new_user, "message": "User created successfully"}

@app.get("/users")
def get_all_users():
    return {"users": users, "count": len(users)}

@app.get("/users/{user_id}")
def get_user(user_id: int):
    user = next((u for u in users if u["id"] == user_id), None)
    if user:
        return user
    return {"error": "User not found"}