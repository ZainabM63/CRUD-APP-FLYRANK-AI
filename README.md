

# Created By : ZAINAB MUGHAL

# To-Do CRUD API (PostgreSQL & Docker-Backed)

A fast, fully containerized CRUD API built with FastAPI, PostgreSQL, and Docker Compose.

## Why PostgreSQL & Docker?
* **Containerized Infrastructure:** Both the FastAPI application and the PostgreSQL database run inside isolated Docker containers, managed seamlessly with a single command.
* **Persistence:** Uses Docker volumes (`taskdata`) so your task records survive container restarts and shutdowns.

## How to Run with Docker Compose
1. Ensure Docker Desktop is running.
2. In your project root directory, run the following command to build and start the entire stack:
   ```bash
   docker compose up --build

```

## Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/` | API Root Information |
| GET | `/health` | Server Health Status |
| GET | `/tasks` | List all tasks (from PostgreSQL) |
| GET | `/tasks/{id}` | Get single task (parameterized query) |
| POST | `/tasks` | Create task (stored in PostgreSQL) |
| PUT | `/tasks/{id}` | Update task (PostgreSQL UPDATE) |
| DELETE | `/tasks/{id}` | Delete task (PostgreSQL DELETE) |

# Swagger UI

Interactive docs available at http://localhost:8000/docs.

# Database Inspection

The database container can be inspected via CLI or database tools connected to port `5433`:

```bash
docker exec -it taskdb psql -U postgres -d tasks -c "SELECT * FROM tasks;"

```

*[Insert Screenshot of your Swagger UI / Docker logs here]*

# Example SQL Query Executed

```sql
SELECT * FROM tasks WHERE done = TRUE;

```

*Result:* Fetches only the tasks marked as completed directly from the PostgreSQL database.

# EXAMPLE

#### HTTP/1.1 200 OK

#### date: Wed, 05 Aug 2026 03:22:00 GMT

#### server: uvicorn

#### content-length: 151

#### content-type: application/json

```json
{"name":"TASK API","version":"1.0.0","endpoints":["/tasks","/health","/docs"]}

```

```

```