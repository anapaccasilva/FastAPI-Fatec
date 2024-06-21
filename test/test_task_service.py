import pytest
from unittest.mock import Mock
from sqlalchemy.orm import Session
from services.task_services import task_service  # Importa o serviço de tarefas
from models.task_model import Task  # Importa o modelo de tarefa
from repositories.task_repositories import task_repository  # Importa o repositório de tarefas

# Fixture do pytest para mockar o repositório de tarefas
@pytest.fixture
def mock_task_repository():
    return Mock(spec=task_repository)

# Teste para a criação de uma nova tarefa
def test_create_task(mock_task_repository):
    # Mock da sessão do banco de dados
    db = Mock(spec=Session)
    # Dados da tarefa a ser criada
    task_data = {"titulo": "New Task", "descricao": "Task Description", "status": "Pendente"}
    # Instância da tarefa criada
    task_instance = Task(id=1, **task_data)
    # Configura o mock para retornar a instância da tarefa criada
    mock_task_repository.create_task.return_value = task_instance

    # Sobrescreve o repositório do serviço de tarefas com o mock
    task_service.task_repository = mock_task_repository
    # Chama o serviço para criar a tarefa
    task = task_service.create_task(db, **task_data)

    # Verifica se a tarefa foi criada com os dados corretos
    assert task.titulo == "New Task"

# Teste para obter uma tarefa específica pelo ID
def test_get_task(mock_task_repository):
    # Mock da sessão do banco de dados
    db = Mock(spec=Session)
    # Instância da tarefa a ser obtida
    task_instance = Task(id=1, titulo="New Task", descricao="Task Description", status="Pendente")
    # Configura o mock para retornar a instância da tarefa
    mock_task_repository.get_task.return_value = task_instance

    # Sobrescreve o repositório do serviço de tarefas com o mock
    task_service.task_repository = mock_task_repository
    # Chama o serviço para obter a tarefa pelo ID
    task = task_service.get_task(db, 1)
    
    print(task)
    # Verifica se a tarefa obtida possui os dados corretos
    assert task.titulo == "New Task"
    # Verifica se o método do repositório foi chamado corretamente
    mock_task_repository.get_task.assert_called_once_with(db, 1)

# Teste para obter todas as tarefas
def test_get_tasks(mock_task_repository):
    # Mock da sessão do banco de dados
    db = Mock(spec=Session)
    # Configura o mock para retornar uma lista de tarefas
    mock_task_repository.get_tasks.return_value = [Task(id=1, titulo="New Task", descricao="Task Description", status="Pendente")]

    # Sobrescreve o repositório do serviço de tarefas com o mock
    task_service.task_repository = mock_task_repository
    # Chama o serviço para obter todas as tarefas
    tasks = task_service.get_tasks(db)

    # Verifica se a lista de tarefas obtida possui os dados corretos
    assert len(tasks) == 1
    assert tasks[0].titulo == "New Task"

# Teste para atualizar uma tarefa específica pelo ID
def test_update_task(mock_task_repository):
    # Mock da sessão do banco de dados
    db = Mock(spec=Session)
    # Dados atualizados da tarefa
    updated_task_data = {"titulo": "Updated Task", "descricao": "Updated Description", "status": "Concluída"}
    # Configura o mock para retornar a tarefa atualizada
    mock_task_repository.update_task.return_value = Task(id=1, **updated_task_data)

    # Sobrescreve o repositório do serviço de tarefas com o mock
    task_service.task_repository = mock_task_repository
    # Chama o serviço para atualizar a tarefa
    task = task_service.update_task(db, 1, **updated_task_data)

    # Verifica se a tarefa foi atualizada com os dados corretos
    assert task.titulo == "Updated Task"
    assert task.descricao == "Updated Description"
    assert task.status == "Concluída"

# Teste para deletar uma tarefa específica pelo ID
def test_delete_task(mock_task_repository):
    # Mock da sessão do banco de dados
    db = Mock(spec=Session)
    # Configura o mock para retornar None (tarefa deletada com sucesso)
    mock_task_repository.delete_task.return_value = None

    # Sobrescreve o repositório do serviço de tarefas com o mock
    task_service.task_repository = mock_task_repository
    # Chama o serviço para deletar a tarefa
    result = task_service.delete_task(db, 1)

    # Verifica se o resultado da deleção é conforme o esperado
    assert result is None
    # Verifica se o método do repositório foi chamado corretamente
    mock_task_repository.delete_task.assert_called_once_with(db, 1)
