import pytest
from unittest.mock import Mock
from sqlalchemy.orm import Session
from services.task_services import task_service
from models.task_model import Task
from repositories.task_repositories import task_repository

@pytest.fixture
def mock_task_repository():
    return Mock(spec=task_repository)

def test_create_task(mock_task_repository):
    db = Mock(spec=Session)
    task_data = {"titulo": "New Task", "descricao": "Task Description", "status": "Pendente"}
    task_instance = Task(id=1, **task_data)
    mock_task_repository.create_task.return_value = task_instance

    task_service.task_repository = mock_task_repository
    task = task_service.create_task(db, **task_data)

    assert task.titulo == "New Task"


def test_get_task(mock_task_repository):
    db = Mock(spec=Session)
    task_instance = Task(id=1, titulo="New Task", descricao="Task Description", status="Pendente")
    mock_task_repository.get_task.return_value = task_instance

    task_service.task_repository = mock_task_repository
    task = task_service.get_task(db, 1)
    print(task)
    assert task.titulo == "New Task"
    mock_task_repository.get_task.assert_called_once_with(db, 1)

def test_get_tasks(mock_task_repository):
    db = Mock(spec=Session)
    mock_task_repository.get_tasks.return_value = [Task(id=1, titulo="New Task", descricao="Task Description", status="Pendente")]

    task_service.task_repository = mock_task_repository
    tasks = task_service.get_tasks(db)

    assert len(tasks) == 1
    assert tasks[0].titulo == "New Task"

def test_update_task(mock_task_repository):
    db = Mock(spec=Session)
    updated_task_data = {"titulo": "Updated Task", "descricao": "Updated Description", "status": "Concluída"}
    mock_task_repository.update_task.return_value = Task(id=1, **updated_task_data)

    task_service.task_repository = mock_task_repository
    task = task_service.update_task(db, 1, **updated_task_data)

    assert task.titulo == "Updated Task"
    assert task.descricao == "Updated Description"
    assert task.status == "Concluída"

def test_delete_task(mock_task_repository):
    db = Mock(spec=Session)
    mock_task_repository.delete_task.return_value = None

    task_service.task_repository = mock_task_repository
    result = task_service.delete_task(db, 1)

    assert result.titulo == "Updated Task"
