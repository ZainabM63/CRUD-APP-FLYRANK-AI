from typing import List
from fastapi import FastAPI, HTTPException
from fastapi import status

app=FastAPI(
    title="TASK API",
    description="This is a simple in-memory TODO CRUD API",
    version="1.0.0")
    
tasks_db=[{"id":1,"title":"Buy groceries","done":False},{"id":1,"title":"Read book","done":True},{"id":3,"title":"Write code","done":False}
          ]
@app.get("/")
def read_root():
    return {"name": " TASK API",
            "version":"1.0.0",
            "endpoints":["/tasks","/health","/docs"]}

@app.get("/health")
def health_check():
    return{"status":"ok"}

@app.get("/tasks")
def get_tasks():
    return tasks_db

@app.get("/tasks/{id}")
def get_task(id: int):
    for task in tasks_db:
        if task["id"] == id:
            return task
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task with id {id} not found"
    )