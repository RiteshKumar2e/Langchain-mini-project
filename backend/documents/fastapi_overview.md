# FastAPI Overview

## What is FastAPI?

FastAPI is a modern, fast (high-performance) web framework for building APIs with Python based on standard Python type hints. It was created by Sebastián Ramírez and first released in 2018.

FastAPI is built on top of:
- **Starlette**: For the web parts
- **Pydantic**: For data validation and serialization

## Key Features

- **Fast**: Very high performance, on par with NodeJS and Go
- **Fast to code**: Development speed increase of 200-300%
- **Fewer bugs**: Reduce human-induced errors
- **Intuitive**: Great editor support with autocompletion
- **Easy**: Designed to be easy to use and learn
- **Short**: Minimize code duplication
- **Robust**: Production-ready code with automatic interactive documentation
- **Standards-based**: Based on OpenAPI and JSON Schema

## Creating a Basic FastAPI App

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
```

## Path Parameters and Query Parameters

```python
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}

@app.get("/search")
def search(q: str, skip: int = 0, limit: int = 10):
    return {"q": q, "skip": skip, "limit": limit}
```

## Request Body with Pydantic

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str = None
    price: float

@app.post("/items/")
def create_item(item: Item):
    return item
```

## Async Support

FastAPI supports async/await natively:

```python
@app.get("/async-endpoint")
async def async_endpoint():
    result = await some_async_operation()
    return {"result": result}
```

## Dependency Injection

```python
from fastapi import Depends

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/items/")
def read_items(db: Session = Depends(get_db)):
    return db.query(Item).all()
```

## CORS Configuration

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Automatic Documentation

FastAPI automatically generates:
- **Swagger UI**: Available at `/docs`
- **ReDoc**: Available at `/redoc`
- **OpenAPI schema**: Available at `/openapi.json`

## HTTP Status Codes

```python
from fastapi import HTTPException

@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]
```

## Running FastAPI

```bash
# Install
pip install fastapi uvicorn

# Run
uvicorn main:app --reload

# Production
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## FastAPI vs Flask vs Django

| Feature | FastAPI | Flask | Django |
|---------|---------|-------|--------|
| Performance | Very High | Medium | Medium |
| Async Support | Native | Limited | Limited |
| Type Hints | Yes | No | No |
| Auto Docs | Yes | No | No |
| Learning Curve | Low-Medium | Low | High |
| Use Case | APIs | APIs/Web | Full-stack Web |
