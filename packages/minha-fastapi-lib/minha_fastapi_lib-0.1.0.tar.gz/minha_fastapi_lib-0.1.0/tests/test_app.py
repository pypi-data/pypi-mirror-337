from fastapi.testclient import TestClient
from src.minha_api_lib import create_app

client = TestClient(create_app())

def test_exemplo_endpoint():
    response = client.get("/exemplo/")
    assert response.status_code == 200
    assert response.json() == {"message": "Olá do módulo exemplo!"}