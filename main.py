from fastapi import FastAPI, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html
from starlette.responses import RedirectResponse, JSONResponse
from controller.task_controller import task_router

# Cria uma instância da aplicação FastAPI
app = FastAPI(
    title="Task API",
    description="Tarefas",
    version="1.0.0",
    openapi_url="/openapi.json",
    docs_url=None,  # Desativa a URL padrão do Swagger UI
    redoc_url=None,  # Desativa a URL padrão do ReDoc
    contact={
        "name": "Ana Paula Pacca",
        "email": "ana.pacca.silva@gmail.com",
        "url": "https://www.linkedin.com/in/ana-paula-pacca/"
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    },
    servers=[
        {
            "url": "http://localhost:8000",
            "description": "Development server"
        },
    ],
)

# Inclui o roteador das tarefas na aplicação
app.include_router(task_router)

# Handler para exceções HTTP, retorna uma resposta JSON com o status e a mensagem de erro
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": str(exc.detail)}
    )

# Handler para exceções gerais, retorna uma resposta JSON com status 500 e uma mensagem de erro genérica
@app.exception_handler(Exception)
async def general_exception_handler(request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "An unexpected error occurred"}
    )

# Redireciona a raiz da aplicação para a documentação Swagger UI
@app.get("/", tags=["Redirect"], include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")

# Retorna a interface Swagger UI personalizada
@app.get("/docs", tags=["Redirect"], include_in_schema=False)
async def get_swagger_ui():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Swagger UI"
    )

# Handler para a rota do JSON do OpenAPI
@app.get("/openapi.json", tags=["Redirect"], include_in_schema=False)
async def get_openapi():
    return get_swagger_ui(
        title="Tasks API",
        version="1.0.0",
        description="Tarefas",
        routes=app.routes,
    )

# Executa a aplicação usando Uvicorn
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
