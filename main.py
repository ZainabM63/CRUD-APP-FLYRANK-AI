from typing import List, Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv
import psycopg
from psycopg.rows import dict_row

app = FastAPI(
    title="TASK API",
    description="This is a PostgreSQL-backed TODO CRUD API",
    version="1.0.0"
)

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    # Use dict_row so we can access columns by name (e.g., row["id"])
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create the tasks table if it is missing
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            done BOOLEAN DEFAULT FALSE
        )
    """)
    
    # Seed 3 initial tasks only if the table is empty
    cursor.execute("SELECT COUNT(*) FROM tasks;")
    count = cursor.fetchone()['count']
    if count == 0:
        cursor.executemany(
            "INSERT INTO tasks (title, done) VALUES (%s, %s)",
            [
                ("Learn FastAPI", False),
                ("Set up Postgres", True),
                ("Containerize with Docker", False)
            ]
        )
    
    conn.commit()
    cursor.close()
    conn.close()

# Run this on app startup
init_db()

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1)

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1)
    done: Optional[bool] = None

@app.get("/")
def read_root():
    return {
        "name": "TASK API",
        "version": "1.0.0",
        "endpoints": ["/tasks", "/health", "/docs"]
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/tasks")
def get_tasks():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, done FROM tasks")
    rows = cursor.fetchall()
    conn.close()
    return rows

@app.get("/tasks/{id}")
def get_task(id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Postgres uses %s placeholders instead of ?
    cursor.execute("SELECT id, title, done FROM tasks WHERE id = %s", (id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {id} not found"
        )
        
    return row

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task_in: TaskCreate):
    if not task_in.title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Use RETURNING id to capture the auto-generated primary key in Postgres
    cursor.execute(
        "INSERT INTO tasks (title, done) VALUES (%s, %s) RETURNING id, title, done", 
        (task_in.title.strip(), False)
    )
    new_task = cursor.fetchone()
    conn.commit()
    conn.close()
    
    return new_task

@app.put("/tasks/{id}")
def update_task(id: int, task_in: TaskUpdate):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if task exists first
    cursor.execute("SELECT id, title, done FROM tasks WHERE id = %s", (id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail=f"Task {id} not found")
    
    current_title = row["title"]
    current_done = row["done"]
    
    if task_in.title is not None:
        if not task_in.title.strip():
            conn.close()
            raise HTTPException(status_code=400, detail="Title cannot be empty")
        current_title = task_in.title.strip()
        
    if task_in.done is not None:
        current_done = task_in.done
        
    # Parameterized update statement using %s
    cursor.execute(
        "UPDATE tasks SET title = %s, done = %s WHERE id = %s RETURNING id, title, done",
        (current_title, current_done, id)
    )
    updated_task = cursor.fetchone()
    conn.commit()
    conn.close()
    
    return updated_task

@app.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if task exists first
    cursor.execute("SELECT id FROM tasks WHERE id = %s", (id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail=f"Task {id} not found")
        
    # Parameterized delete statement using %s
    cursor.execute("DELETE FROM tasks WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    
    return None