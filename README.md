# Sistema de Gerenciamento de Tarefas com FastAPI

## Objetivo
Desenvolver uma API para gerenciamento de tarefas utilizando FastAPI, aplicando conceitos de controllers, services e repositories.

## Descrição do Projeto
A API permite a criação, leitura, atualização e exclusão de tarefas, cada uma com:
- **id**: Identificador único da tarefa (integer, primary key)
- **title**: Título da tarefa (string)
- **description**: Descrição da tarefa (string)
- **status**: Status da tarefa (string: "Pendente", "Em Progresso", "Concluída")
- **created_at**: Data de criação da tarefa (datetime)

## Componentes
- **Controllers**: Definem os endpoints da API.
- **Services**: Contêm a lógica de negócios e validações.
- **Repositories**: Gerenciam a interação com o banco de dados.

## Requisitos
- Python 3.10+
- FastAPI
- SQLAlchemy
- SQLite

## Endpoints
- **POST /tasks/**: Criar uma nova tarefa.
- **GET /tasks/**: Listar todas as tarefas.
- **GET /tasks/{task_id}**: Obter detalhes de uma tarefa específica por ID.
- **PUT /tasks/{task_id}**: Atualizar uma tarefa específica por ID.
- **DELETE /tasks/{task_id}**: Deletar uma tarefa específica por ID.
