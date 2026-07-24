from typing import List, Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app=FastAPI(
    title="TASK API",
    description="This is a simple in-memory TODO CRUD API",
    version="1.0.0")

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1)

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1)
    done: Optional[bool] = None

def get_next_id() -> int:
    return max([t["id"] for t in tasks_db], default=0) + 1

tasks_db=[{"id":1,"title":"Buy groceries","done":False},
          {"id":1,"title":"Read book","done":True},
          {"id":3,"title":"Write code","done":False}
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

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task_in: TaskCreate):
    if not task_in.title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    new_task = {"id": get_next_id(), "title": task_in.title.strip(), "done": False}
    tasks_db.append(new_task)
    return new_task

@app.put("/tasks/{id}")
def update_task(id: int, task_in: TaskUpdate):
    task = next((t for t in tasks_db if t["id"] == id), None)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task {id} not found")
    
    if task_in.title is not None:
        if not task_in.title.strip():
            raise HTTPException(status_code=400, detail="Title cannot be empty")
        task["title"] = task_in.title.strip()
    if task_in.done is not None:
        task["done"] = task_in.done
    return task

@app.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id: int):
    global tasks_db
    task = next((t for t in tasks_db if t["id"] == id), None)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task {id} not found")
    tasks_db = [t for t in tasks_db if t["id"] != id]
    return None