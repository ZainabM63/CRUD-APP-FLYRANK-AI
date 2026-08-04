from typing import List, Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

import sqlite3

app=FastAPI(
    title="TASK API",
    description="This is a simple in-memory TODO CRUD API",
    version="1.0.0")

DB_FILE = "tasks.db"

def get_db_connection():
    """Helper function to open a connection to the SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # 1. Create table if missing
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL
        )
    """)
    
    # 2. Check row count to seed only once
    cursor.execute("SELECT COUNT(*) FROM tasks")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO tasks (title, done) VALUES (?, ?)", [
            ("Buy groceries", 0),
            ("Read book", 1),
            ("Write code", 0)
        ])
        conn.commit()
    conn.close()

# Run it immediately when the app starts up
init_db()

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
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, done FROM tasks")
    rows = cursor.fetchall()
    conn.close()
    
    # Convert database rows into dictionaries and convert done (0/1) back to boolean (False/True)
    return [{"id": row[0], "title": row[1], "done": bool(row[2])} for row in rows]

@app.get("/tasks/{id}")
def get_task(id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Parameterized query protects against SQL injection
    cursor.execute("SELECT id, title, done FROM tasks WHERE id = ?", (id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {id} not found"
        )
        
    return {"id": row["id"], "title": row["title"], "done": bool(row["done"])}

# Stage 2: Create new tasks and store them in the database
@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task_in: TaskCreate):
    if not task_in.title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Insert new task into SQLite; set initial done status to 0 (False)
    cursor.execute(
        "INSERT INTO tasks (title, done) VALUES (?, ?)", 
        (task_in.title.strip(), 0)
    )
    conn.commit()
    
    # Grab the unique ID that the database just assigned to this new row
    new_id = cursor.lastrowid
    conn.close()
    
    return {"id": new_id, "title": task_in.title.strip(), "done": False}

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