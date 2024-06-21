from sqlalchemy.orm import Session

from fastapi import HTTPException
from pydantic import TypeAdapter
from sqlalchemy.exc import IntegrityError
from domain.model.models import Task
from repository.task_repository import TaskRepository

# Classe de serviço para gerenciar a lógica de negócios relacionada às tarefas
class TaskService():

    # Método para criar uma nova tarefa
    def create_task(db: Session, title: str, description: str, status: str):
        # Cria uma instância da tarefa com os dados fornecidos
        task = Task(title=title, description=description, status=status)
        # Chama o repositório para salvar a tarefa no banco de dados
        return TaskRepository.create_task(db, task)

    # Método para obter uma tarefa específica pelo ID
    def get_task(db: Session, task_id: int):
        # Chama o repositório para ler a tarefa a partir do banco de dados
        return TaskRepository.read_task(db, task_id)

    # Método para obter todas as tarefas
    def get_tasks(db: Session):
        # Chama o repositório para encontrar todas as tarefas no banco de dados
        return TaskRepository.find_all_task(db)

    # Método para atualizar uma tarefa específica pelo ID
    def update_task(db: Session, task_id: int, title: str = None, description: str = None, status: str = None):
        # Cria um dicionário com os dados da tarefa que foram fornecidos
        task_data = {k: v for k, v in {"title": title, "description": description, "status": status}.items() if v is not None}
        # Chama o repositório para atualizar a tarefa no banco de dados com os novos dados
        return TaskRepository.update_task(db, task_id, task_data)

    # Método para deletar uma tarefa específica pelo ID
    def delete_task(db: Session, task_id: int):
        # Chama o repositório para deletar a tarefa do banco de dados
        return TaskRepository.delete_task(db, task_id)
