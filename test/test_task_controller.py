import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, ANY
from main import app
from services.task_services import task_service  # Importa o serviço de tarefas
from models.task_model import Task  # Importa o modelo de tarefa
from schemas.task_schema import TaskCreate, TaskUpdate  # Importa os esquemas para criar e atualizar tarefas

# Cria um cliente de teste para a aplicação FastAPI
client = TestClient(app)

# Fixture do pytest para mockar o serviço de tarefas
@pytest.fixture
def mock_task_service():
    return Mock(spec=task_service)

# Teste para a criação de uma nova tarefa
def test_create_task(mock_task_service):
    # Sobrescreve a dependência do serviço de tarefas com o mock
    client.app.dependency_overrides[task_service] = lambda: mock_task_service
    # Dados da tarefa a ser criada
    task_data = TaskCreate(titulo="New Task", descricao="Task Description", status="Pendente")
    # Configura o mock para retornar uma tarefa com ID 1
    mock_task_service.create_task.return_value = Task(id=1, **task_data.dict())

    # Faz a requisição POST para criar a tarefa
    response = client.post("/tasks/", json=task_data.dict())

    print(response.status_code)
    print(response.json()['titulo'])
    # Verifica se o status da resposta é 200 (OK)
    assert response.status_code == 200
    # Verifica se o título da tarefa criada é "New Task"
    assert response.json()['titulo'] == "New Task"

# Teste para obter todas as tarefas
def test_read_tasks(mock_task_service):
    # Sobrescreve a dependência do serviço de tarefas com o mock
    client.app.dependency_overrides[task_service] = lambda: mock_task_service
    # Configura o mock para retornar uma lista de tarefas
    mock_task_service.get_tasks.return_value = [Task(id=1, titulo="New Task", descricao="Task Description", status="Pendente")]
    # Faz a requisição GET para obter todas as tarefas
    response = client.get("/tasks/")
    
    print(response.json())

    # Verifica se o status da resposta é 200 (OK)
    assert response.status_code == 200
    # Verifica se há pelo menos uma tarefa na resposta
    assert len(response.json()) >= 1
    # Verifica se o título da primeira tarefa é "New Task"
    assert response.json()[0]['titulo'] == "New Task"

# Teste para obter uma tarefa específica pelo ID
def test_read_task(mock_task_service):
    # Sobrescreve a dependência do serviço de tarefas com o mock
    client.app.dependency_overrides[task_service] = lambda: mock_task_service
    # Configura o mock para retornar uma tarefa específica
    mock_task_service.get_task.return_value = Task(id=1, titulo="New Task", descricao="Task Description", status="Pendente")

    # Faz a requisição GET para obter a tarefa pelo ID
    response = client.get("/tasks/1")
    
    # Verifica se o status da resposta é 200 (OK)
    assert response.status_code == 200
    # Verifica se o título da tarefa é "New Task"
    assert response.json()['titulo'] == "New Task"

# Teste para o caso em que a tarefa não é encontrada
def test_read_task_not_found(mock_task_service):
    # Sobrescreve a dependência do serviço de tarefas com o mock
    client.app.dependency_overrides[task_service] = lambda: mock_task_service
    # Configura o mock para retornar None (tarefa não encontrada)
    mock_task_service.get_task.return_value = None

    # Faz a requisição GET para obter uma tarefa que não existe
    response = client.get("/tasks/999")
    print(response.json())
    # Verifica se o status da resposta é 404 (Não encontrado)
    assert response.status_code == 404
    # Verifica se a mensagem de erro é "Tarefa não encontrada..."
    assert response.json()['message'] == "Tarefa não encontrada..."

# Teste para atualizar uma tarefa específica pelo ID
def test_update_task(mock_task_service):
    # Sobrescreve a dependência do serviço de tarefas com o mock
    client.app.dependency_overrides[task_service] = lambda: mock_task_service
    # Dados atualizados da tarefa
    updated_task = TaskUpdate(titulo="Updated Task", descricao="Updated Description", status="Concluída")
    # Configura o mock para retornar a tarefa atualizada
    mock_task_service.update_task.return_value = Task(id=1, **updated_task.dict(exclude_unset=True))

    # Faz a requisição PUT para atualizar a tarefa
    response = client.put("/tasks/1", json=updated_task.dict(exclude_unset=True))

    # Verifica se o status da resposta é 200 (OK)
    assert response.status_code == 200
    # Verifica se o título da tarefa atualizada é "Updated Task"
    assert response.json()['titulo'] == "Updated Task"

# Teste para deletar uma tarefa específica pelo ID
def test_delete_task(mock_task_service):
    # Sobrescreve a dependência do serviço de tarefas com o mock
    client.app.dependency_overrides[task_service] = lambda: mock_task_service
    # Configura o mock para retornar None (tarefa deletada com sucesso)
    mock_task_service.delete_task.return_value = None

    # Faz a requisição DELETE para deletar a tarefa
    response = client.delete("/tasks/1")

    # Verifica se o status da resposta é 200 (OK)
    assert response.status_code == 200
    # Verifica se a mensagem de confirmação é "Tarefa excluída!"
    assert response.json()['detail'] == "Tarefa excluída!"
