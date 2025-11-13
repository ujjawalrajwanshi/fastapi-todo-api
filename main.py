from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

app = FastAPI(
    title="Todo API",
    description="A complete CRUD API for managing todos",
    version="1.0.0"
)

# Models
class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class Todo(TodoCreate):
    id: int
    created_at: str
    updated_at: str

# In-memory database
todos = []
todo_id_counter = 1

# Helper function
def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# CREATE - Add new todo
@app.post("/todos", response_model=Todo, status_code=201)
def create_todo(todo: TodoCreate):
    """Create a new todo item"""
    global todo_id_counter
    
    new_todo = {
        "id": todo_id_counter,
        "title": todo.title,
        "description": todo.description,
        "completed": todo.completed,
        "created_at": get_current_time(),
        "updated_at": get_current_time()
    }
    
    todos.append(new_todo)
    todo_id_counter += 1
    
    return new_todo

# READ - Get all todos
@app.get("/todos", response_model=List[Todo])
def get_todos(completed: Optional[bool] = None):
    """
    Get all todos, optionally filter by completion status
    
    - completed=true: Get only completed todos
    - completed=false: Get only pending todos
    - No param: Get all todos
    """
    if completed is None:
        return todos
    
    return [t for t in todos if t["completed"] == completed]

# READ - Get single todo
@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: int):
    """Get a specific todo by ID"""
    todo = next((t for t in todos if t["id"] == todo_id), None)
    
    if not todo:
        raise HTTPException(status_code=404, detail=f"Todo with id {todo_id} not found")
    
    return todo

# UPDATE - Update entire todo
@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, todo_update: TodoCreate):
    """Update a todo completely"""
    todo = next((t for t in todos if t["id"] == todo_id), None)
    
    if not todo:
        raise HTTPException(status_code=404, detail=f"Todo with id {todo_id} not found")
    
    # Update fields
    todo["title"] = todo_update.title
    todo["description"] = todo_update.description
    todo["completed"] = todo_update.completed
    todo["updated_at"] = get_current_time()
    
    return todo

# PATCH - Mark as complete
@app.patch("/todos/{todo_id}/complete", response_model=Todo)
def mark_complete(todo_id: int):
    """Mark a todo as completed"""
    todo = next((t for t in todos if t["id"] == todo_id), None)
    
    if not todo:
        raise HTTPException(status_code=404, detail=f"Todo with id {todo_id} not found")
    
    todo["completed"] = True
    todo["updated_at"] = get_current_time()
    
    return todo

# DELETE - Delete todo
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    """Delete a todo"""
    global todos
    
    todo = next((t for t in todos if t["id"] == todo_id), None)
    
    if not todo:
        raise HTTPException(status_code=404, detail=f"Todo with id {todo_id} not found")
    
    todos = [t for t in todos if t["id"] != todo_id]
    
    return {"message": f"Todo {todo_id} deleted successfully"}

# STATS - Get statistics
@app.get("/stats")
def get_stats():
    """Get todo statistics"""
    total = len(todos)
    completed = len([t for t in todos if t["completed"]])
    pending = total - completed
    
    return {
        "total": total,
        "completed": completed,
        "pending": pending,
        "completion_rate": f"{(completed/total*100):.1f}%" if total > 0 else "0%"
    }

# Root endpoint
@app.get("/")
def root():
    """API information"""
    return {
        "name": "Todo API",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "todos": "/todos",
            "stats": "/stats"
        }
    }
