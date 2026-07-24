# To-Do CRUD API

A fast in-memory CRUD API built with FastAPI.

## How to Install & Run
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install "fastapi[standard]" uvicorn
fastapi dev main.py

Method,Endpoint,Description
GET,/,API Root Information
GET,/health,Server Health Status
GET,/tasks,List all tasks
GET,/tasks/{id},Get single task
POST,/tasks,Create task
PUT,/tasks/{id},Update task
DELETE,/tasks/{id},Delete task
 ```

# Swagger UI

Interactive docs available at http://localhost:8000/docs.