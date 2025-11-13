# fastapi-todo-api

# Todo API

A complete RESTful API for managing todo items built with FastAPI.

## Features

✅ **CREATE** - Add new todos
✅ **READ** - Get all todos or filter by status
✅ **UPDATE** - Modify existing todos
✅ **DELETE** - Remove todos
✅ **STATS** - View completion statistics
✅ **Automatic validation** with Pydantic
✅ **Interactive docs** at /docs


# Run the server
uvicorn main:app --reload
```

Server runs at: `http://localhost:8000`

## API Endpoints

### Create Todo
**POST** `/todos`
```json
{
  "title": "Learn FastAPI",
  "description": "Complete the tutorial",
  "completed": false
}
```

### Get All Todos
**GET** `/todos`
- Optional query: `?completed=true` or `?completed=false`

### Get Single Todo
**GET** `/todos/{id}`

### Update Todo
**PUT** `/todos/{id}`
```json
{
  "title": "Updated title",
  "description": "Updated description",
  "completed": true
}
```

### Mark as Complete
**PATCH** `/todos/{id}/complete`

### Delete Todo
**DELETE** `/todos/{id}`

### Get Statistics
**GET** `/stats`

## Interactive Documentation

Visit `http://localhost:8000/docs` for:
- Interactive API testing
- Automatic request/response examples
- Try all endpoints in browser


## Tech Stack

- **FastAPI** - Modern Python web framework
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

## What I Learned

- RESTful API design principles
- CRUD operations in FastAPI
- Request/response validation with Pydantic
- HTTP status codes (200, 201, 404)
- Path and query parameters
- Error handling with HTTPException


