from datetime import datetime, timezone
from fastapi import APIRouter, status
from models.schemas import HealthResponse

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Verificar integridade da API",
    description="Endpoint público para verificação de status e disponibilidade do serviço."
)
async def get_health():
    """Retorna o status operacional da API, versão e timestamp atual."""
    return HealthResponse(
        status="ok",
        version="1.0.0",
        service="Customer Support Ticket API - PB TP1",
        timestamp=datetime.now(timezone.utc)
    )