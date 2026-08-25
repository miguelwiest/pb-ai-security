import pytest
import sys
from pathlib import Path

# Adiciona o diretório fastapi ao sys.path
fastapi_dir = Path(__file__).resolve().parent.parent / "fastapi"
if str(fastapi_dir) not in sys.path:
    sys.path.insert(0, str(fastapi_dir))

from fastapi.testclient import TestClient
from main import app
from security.auth import ADMIN_PASSWORD_PLAIN

client = TestClient(app)


def test_root():
    """Testa a rota raiz da API."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["docs"] == "/docs"


def test_health_check():
    """Testa o endpoint GET /health."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["version"] == "1.0.0"
    assert "timestamp" in data


def test_auth_login_invalid_credentials():
    """Testa falha de autenticação com credenciais incorretas."""
    response = client.post(
        "/auth/token",
        data={"username": "wrong_user", "password": "wrong_password"}
    )
    assert response.status_code == 401
    assert "detail" in response.json()


def test_auth_login_success():
    """Testa autenticação bem-sucedida com credenciais admin in-code."""
    response = client.post(
        "/auth/token",
        data={"username": "admin", "password": ADMIN_PASSWORD_PLAIN}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert len(data["access_token"]) > 20


def test_predict_unauthorized():
    """Testa a rota /predict sem fornecer token (deve retornar 401)."""
    response = client.post(
        "/predict",
        json={"text": "Não consigo resetar minha senha de acesso."}
    )
    assert response.status_code == 401


def test_predict_invalid_token():
    """Testa a rota /predict com token malformado ou adulterado."""
    response = client.post(
        "/predict",
        headers={"Authorization": "Bearer token_invalido_12345"},
        json={"text": "Problema com cobrança indevida."}
    )
    assert response.status_code == 401


def test_predict_authorized_success():
    """Testa a rota /predict com token JWT válido emitido."""
    # 1. Obtém o token
    login_resp = client.post(
        "/auth/token",
        data={"username": "admin", "password": ADMIN_PASSWORD_PLAIN}
    )
    token = login_resp.json()["access_token"]

    # 2. Executa a predição protegida
    predict_payload = {
        "text": "O aplicativo apresenta erro 504 e fecha sozinho ao abrir."
    }
    response = client.post(
        "/predict",
        headers={"Authorization": f"Bearer {token}"},
        json=predict_payload
    )
    assert response.status_code == 200
    data = response.json()
    assert data["input_text"] == predict_payload["text"]
    assert data["predicted_intent"] == "Technical issue"
    assert data["confidence"] >= 0.7
    assert "MockIntentClassifier" in data["simulated_model"]
