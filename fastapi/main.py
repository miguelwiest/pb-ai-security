import sys
import os
from pathlib import Path

# Garante que os módulos locais em fastapi/ sejam encontrados
current_dir = Path(__file__).resolve().parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import health_router, auth_router, predict_router

app = FastAPI(
    title="Customer Support Ticket Intelligent API",
    description=(
        "API para Atendimento ao Cliente com IA - Projeto de Bloco (TP1).\n\n"
        "Esta API disponibiliza endpoints para monitoramento de integridade, "
        "autenticação segura via OAuth2 com tokens JWT e inferência simulada "
        "de intenção de tickets de suporte baseados no 'Customer Support Ticket Dataset'."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuração de CORS para permitir requisições de clientes web autorizados
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro modular de rotas
app.include_router(health_router)
app.include_router(auth_router)
app.include_router(predict_router)


@app.get("/", tags=["Root"])
async def root():
    """Rota raiz com links para documentação interativa e status."""
    return {
        "message": "Customer Support Ticket Intelligent API está em execução.",
        "docs": "/docs",
        "health": "/health",
        "auth": "/auth/token",
        "predict": "/predict"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
