from fastapi.testclient import TestClient

from app.main import app, tasks


client = TestClient(app)


def setup_function() -> None:
    tasks.clear()


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_task_crud() -> None:
    created = client.post("/tasks", json={"title": "Learn FastAPI"})
    assert created.status_code == 201
    task_id = created.json()["id"]

    fetched = client.get(f"/tasks/{task_id}")
    assert fetched.json()["title"] == "Learn FastAPI"

    updated = client.patch(f"/tasks/{task_id}", json={"completed": True})
    assert updated.json()["completed"] is True

    deleted = client.delete(f"/tasks/{task_id}")
    assert deleted.status_code == 204
    assert client.get(f"/tasks/{task_id}").status_code == 404
