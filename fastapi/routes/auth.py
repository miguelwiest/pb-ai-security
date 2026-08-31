from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from models.schemas import Token, User
from security.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    USERS_DB,
    authenticate_user,
    create_access_token,
    get_token_user
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/token",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    summary="Obter Token de Acesso JWT",
    description="Autentica o usuário (form-data com username e password) e retorna o token JWT para rotas protegidas."
)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Recebe as credenciais via form-data (compatível com Swagger UI e OAuth2).
    Apenas o usuário administrador configurado in-code é autenticado com sucesso.
    """
    user = authenticate_user(USERS_DB, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nome de usuário ou senha incorretos",
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="Bearer")


@router.get(
    "/me",
    response_model=User,
    summary="Consultar usuário autenticado",
    description="Retorna informações do perfil autenticado pelo token JWT."
)
async def read_users_me(current_user: User = Depends(get_token_user)):
    return current_user