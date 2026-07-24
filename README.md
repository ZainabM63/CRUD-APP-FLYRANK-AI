# To-Do CRUD API

A fast in-memory CRUD API built with FastAPI.

## How to Install & Run
```bash

pip install "fastapi[standard]" uvicorn
fastapi dev main.py
```

Method,Endpoint,Description
GET,/,API Root Information
GET,/health,Server Health Status
GET,/tasks,List all tasks
GET,/tasks/{id},Get single task
POST,/tasks,Create task
PUT,/tasks/{id},Update task
DELETE,/tasks/{id},Delete task


# Swagger UI

Interactive docs available at http://localhost:8000/docs.

# EXAMPLE

#### HTTP/1.1 200 OK
#### date: Sat, 25 Jul 2026 02:00:00 GMT
#### server: uvicorn
#### content-length: 151
#### content-type: application/json

```bash
{"name":"Task API","version":"1.0","endpoints":["/tasks","/health","/docs"]}