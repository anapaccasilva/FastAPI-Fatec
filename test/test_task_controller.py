import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, ANY
from main import app
from services.task_services import task_service
from models.task_model import Task
from schemas.task_schema import TaskCreate, TaskUpdate

client = TestClient(app)

@pytest.fixture
def mock_task_service():
    return Mock(spec=task_service)

def test_create_task(mock_task_service):
    client.app.dependency_overrides[task_service] = lambda: mock_task_service
    task_data = TaskCreate(titulo="New Task", descricao="Task Description", status="Pendente")
    mock_task_service.create_task.return_value = Task(id=1, **task_data.dict())

    response = client.post("/tasks/", json=task_data.dict())

    print(response.status_code)
    print(response.json()['titulo'])
    assert response.status_code == 200
    assert response.json()['titulo'] == "New Task"

def test_read_tasks(mock_task_service):
    client.app.dependency_overrides[task_service] = lambda: mock_task_service
    mock_task_service.get_tasks.return_value = [Task(id=1, titulo="New Task", descricao="Task Description", status="Pendente")]
    response = client.get("/tasks/")
    
    print(response.json())

    assert response.status_code == 200
    assert len(response.json()) >= 1
    assert response.json()[0]['titulo'] == "New Task"

def test_read_task(mock_task_service):
    client.app.dependency_overrides[task_service] = lambda: mock_task_service
    mock_task_service.get_task.return_value = Task(id=1, titulo="New Task", descricao="Task Description", status="Pendente")

    response = client.get("/tasks/1")
    
    assert response.status_code == 200
    assert response.json()['titulo'] == "New Task"

def test_read_task_not_found(mock_task_service):
    client.app.dependency_overrides[task_service] = lambda: mock_task_service
    mock_task_service.get_task.return_value = None

    response = client.get("/tasks/999")
    print(response.json())
    assert response.status_code == 404
    assert response.json()['message'] == "Tarefa não encontrada..."

def test_update_task(mock_task_service):
    client.app.dependency_overrides[task_service] = lambda: mock_task_service
    updated_task = TaskUpdate(titulo="Updated Task", descricao="Updated Description", status="Concluída")
    mock_task_service.update_task.return_value = Task(id=1, **updated_task.dict(exclude_unset=True))

    response = client.put("/tasks/1", json=updated_task.dict(exclude_unset=True))

    assert response.status_code == 200
    assert response.json()['titulo'] == "Updated Task"

def test_delete_task(mock_task_service):
    client.app.dependency_overrides[task_service] = lambda: mock_task_service
    mock_task_service.delete_task.return_value = None

    response = client.delete("/tasks/1")

    assert response.status_code == 200
    assert response.json()['detail'] == "Tarefa excluída!"
