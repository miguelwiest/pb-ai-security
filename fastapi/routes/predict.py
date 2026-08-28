from datetime import datetime, timezone
from fastapi import APIRouter, Depends, status

from models.schemas import PredictRequest, PredictResponse, User
from security.auth import get_token_user

router = APIRouter(tags=["Machine Learning Prediction"])


def mock_classify_intent(text: str) -> tuple[str, float]:
    """
    Função de simulação de predição de intenção de tickets de suporte.
    Analisa palavras-chave para retornar intenções representativas do dataset
    (Technical issue, Billing inquiry, Cancellation request, Product inquiry, Refund request).
    """
    text_lower = text.lower()
    if any(k in text_lower for k in ["erro", "crash", "bug", "travando", "timeout", "falha", "conect", "bluetooth", "firmware"]):
        return "Technical issue", 0.94
    elif any(k in text_lower for k in ["fatura", "cobrança", "cartão", "pagamento", "invoice", "desconto", "preço"]):
        return "Billing inquiry", 0.91
    elif any(k in text_lower for k in ["cancelar", "cancelamento", "encerrar", "excluir conta", "deletar"]):
        return "Cancellation request", 0.96
    elif any(k in text_lower for k in ["reembolso", "devolução", "estorno", "refund", "devolver"]):
        return "Refund request", 0.93
    elif any(k in text_lower for k in ["compatibilidade", "bateria", "especificação", "dúvida", "funciona", "manual"]):
        return "Product inquiry", 0.88
    else:
        return "Technical issue", 0.75


@router.post(
    "/predict",
    response_model=PredictResponse,
    status_code=status.HTTP_200_OK,
    summary="Simular predição de intenção de ticket",
    description="Rota protegida por JWT. Recebe um texto de ticket e retorna uma intenção simulada correspondente ao domínio do dataset."
)
async def predict_ticket_intent(
    request: PredictRequest,
    current_user: User = Depends(get_token_user)
):
    """
    Endpoint autenticado para classificação de tickets.
    Exige cabeçalho `Authorization: Bearer <token_jwt>`.
    """
    intent, confidence = mock_classify_intent(request.text)

    return PredictResponse(
        input_text=request.text,
        predicted_intent=intent,
        confidence=confidence,
        simulated_model="MockIntentClassifier-v1.0 (Simulation Phase)",
        timestamp=datetime.now(timezone.utc)
    )
