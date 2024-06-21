from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from config.database import get_db
from repository.task_repository import TaskRepository
from service.task_service import TaskService

# Cria um roteador para gerenciar as rotas relacionadas às tarefas
task_router = APIRouter(prefix="/tasks", tags=["tasks"])

# Função de dependência que obtém uma instância do repositório de tarefas a partir da sessão do banco de dados
def get_user_repo(db: Session = Depends(get_db)) -> TaskRepository:
    return TaskRepository(db)

# Rota para criar uma nova tarefa
@task_router.post("/tasks/")
def create_task(title: str, description: str, status: str, db: Session = Depends(get_db)):
    # Chama o serviço de criação de tarefa passando os parâmetros necessários
    return TaskService.create_task(db, title, description, status)

# Rota para ler todas as tarefas
@task_router.get("/tasks/")
def read_tasks(db: Session = Depends(get_db)):
    # Chama o serviço para obter todas as tarefas
    return TaskService.get_tasks(db)

# Rota para ler uma tarefa específica pelo ID
@task_router.get("/tasks/{task_id}")
def read_task(task_id: int, db: Session = Depends(get_db)):
    # Chama o serviço para obter uma tarefa específica pelo ID
    task = TaskService.get_task(db, task_id)
    # Verifica se a tarefa existe; se não, lança uma exceção HTTP 404
    if task is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada...")
    return task

# Rota para atualizar uma tarefa específica pelo ID
@task_router.put("/tasks/{task_id}")
def update_task(task_id: int, title: str = None, description: str = None, status: str = None, db: Session = Depends(get_db)):
    # Chama o serviço para atualizar a tarefa com os novos dados fornecidos
    return TaskService.update_task(db, task_id, title, description, status)

# Rota para deletar uma tarefa específica pelo ID
@task_router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    # Chama o serviço para deletar a tarefa pelo ID
    TaskService.delete_task(db, task_id)
    # Retorna uma mensagem de confirmação
    return {"detail": "Tarefa excluída!"}
