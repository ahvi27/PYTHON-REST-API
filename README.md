# Python Task Manager REST API

A complete beginner-friendly CRUD API made with FastAPI. Data is stored in memory, so it resets whenever the server restarts.

## Run on Linux, macOS, or Windows

Open a terminal inside this project folder, then run:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

Then open:

- API documentation: http://127.0.0.1:8000/docs
- API home: http://127.0.0.1:8000/

Do not open only `/tasks` and expect a web page. It is an API endpoint and returns JSON. Use `/docs` to test every operation with buttons.

## Endpoints

| Method | Path | Purpose |
|---|---|---|
| GET | `/` | Welcome message |
| GET | `/health` | Health check |
| POST | `/tasks` | Create a task |
| GET | `/tasks` | List tasks |
| GET | `/tasks/{task_id}` | Get one task |
| PATCH | `/tasks/{task_id}` | Update part of a task |
| DELETE | `/tasks/{task_id}` | Delete a task |

Filter completed tasks with `/tasks?completed=true`.

## Example request

```bash
curl -X POST http://127.0.0.1:8000/tasks \
  -H 'Content-Type: application/json' \
  -d '{"title":"Learn REST APIs","description":"Build one with FastAPI"}'
```

## Run tests

```bash
python -m pytest
```
