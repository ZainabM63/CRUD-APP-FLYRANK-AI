

# Created By : ZAINAB MUGHAL

# To-Do CRUD API (SQLite-Backed)

A fast, persistent CRUD API built with FastAPI and SQLite[cite: 1].

## Why SQLite?
* **Zero Configuration & Single File:** It runs without a separate server installation, saving all data into a single local file (`tasks.db`)[cite: 1].
* **Persistence:** Unlike an in-memory list which resets every time the server restarts, SQLite saves data to disk so it survives restarts[cite: 1].

## Where the Database Lives
The database file is created automatically as **`tasks.db`** in your project root the first time the app runs[cite: 1]. It is git-ignored so every clone starts with a clean slate[cite: 1].

## How to Install & Run
```bash
pip install "fastapi[standard]" uvicorn
fastapi dev main.py

```

## Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/` | API Root Information |
| GET | `/health` | Server Health Status |
| GET | `/tasks` | List all tasks (from SQLite)

 |
| GET | `/tasks/{id}` | Get single task (parameterized query)

 |
| POST | `/tasks` | Create task (stored in SQLite)

 |
| PUT | `/tasks/{id}` | Update task (SQLite UPDATE)

 |
| DELETE | `/tasks/{id}` | Delete task (SQLite DELETE)

 |

# Swagger UI

Interactive docs available at http://localhost:8000/docs.

# Database Inspection (DB Browser)

The database can be opened directly in DB Browser for SQLite or an online viewer to inspect rows.

*[Insert Screenshot of your database open in DB Browser/Viewer here]*

# Example SQL Query Executed (Stage 4)

```sql
SELECT * FROM tasks WHERE done = 1;

```

*Result:* Fetches only the tasks marked as completed directly from the database.

# EXAMPLE

#### HTTP/1.1 200 OK

#### date: Sat, 25 Jul 2026 02:00:00 GMT

#### server: uvicorn

#### content-length: 151

#### content-type: application/json

```json
{"name":"Task API","version":"1.0","endpoints":["/tasks","/health","/docs"]}

```

```

```