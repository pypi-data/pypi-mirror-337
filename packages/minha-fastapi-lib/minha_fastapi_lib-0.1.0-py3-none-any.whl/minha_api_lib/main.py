from fastapi import FastAPI

app = FastAPI()

from .routers import exemplo

def create_app() -> FastAPI:
    """Cria e configura a aplicação FastAPI"""
    app.include_router(exemplo.router)
    return app

def get_app() -> FastAPI:
    """Retorna a instância da aplicação para uso em servidores ASGI"""
    return create_app()