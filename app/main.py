from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel, Field


app = FastAPI(
    title="Task Manager API",
    description="A beginner-friendly CRUD REST API built with Python and FastAPI.",
    version="1.0.0",
)


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str = Field(default="", max_length=500)
    completed: bool = False


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    completed: bool | None = None


class Task(TaskCreate):
    id: int
    created_at: datetime


tasks: dict[int, Task] = {}
next_id = 1


@app.get("/")
def home() -> dict[str, str]:
    return {"message": "Task Manager API is running", "documentation": "/docs"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy"}


@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate) -> Task:
    global next_id
    task = Task(
        id=next_id,
        created_at=datetime.now(timezone.utc),
        **payload.model_dump(),
    )
    tasks[next_id] = task
    next_id += 1
    return task


@app.get("/tasks", response_model=list[Task])
def list_tasks(completed: bool | None = None) -> list[Task]:
    result = list(tasks.values())
    if completed is not None:
        result = [task for task in result if task.completed == completed]
    return result


def find_task(task_id: int) -> Task:
    task = tasks.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int) -> Task:
    return find_task(task_id)


@app.patch("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, payload: TaskUpdate) -> Task:
    current = find_task(task_id)
    updated = current.model_copy(update=payload.model_dump(exclude_unset=True))
    tasks[task_id] = updated
    return updated


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int) -> Response:
    find_task(task_id)
    del tasks[task_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)
